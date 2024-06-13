from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import baked
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination

from src.globalconfig import GlobalConfig
from src.interceptors import BaseClass
from src.types import InternalError
from src.types.errorcode import *
from src.logger import Logger

from .entities import BaseEntity


class DBRepository(BaseClass):
    def __init__(self):
        super(DBRepository, self).__init__()

        # Get the connection string from global config
        connString = GlobalConfig.instance().DB_CONNECTION

        # Connect to the database
        self.engine = create_engine(connString)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None
        self.bakery = baked.bakery()

    def __openSession(self):
        if self.session is None:
            self.session = self.Session()

    def __closeSession(self):
        if self.session is not None:
            self.session.close()
            self.session = None

    def put(self, entityClass: BaseEntity, obj: dict):
        """
        Put an object into the database

        Parameters
        ----------
        entityClass : BaseEntity
            Entity class
        obj : dict
            An object

        Returns
        -------
        entity : BaseEntity
            The entity that have been putted to the database
        """
        entity = None
        try:
            self.__openSession()

            # Put obj into the database
            entity = entityClass(**obj)
            entity.__table__.create(bind=self.engine, checkfirst=True)

            existed = self.session.query(entity.__class__) \
                .filter(entity.__class__.Code == entity.Code) \
                .first()
            if existed is None:
                # Insert if entity is not exists
                self.session.add(entity)
            else:
                # Update if entity is exists
                existed.copyFrom(entity)
            # Commit change
            self.session.commit()

            # Retrieve new object
            entity = self.getOne(entityClass=entityClass,
                                 filterSpec=[{
                                     'field': 'Code',
                                     'op': '==',
                                     'value': entity.Code
                                 }])
        finally:
            self.__closeSession()
        return entity

    def putBulk(self, entityClass: BaseEntity, objs: list[dict]) -> list[str]:
        """
        Put a list of objects into the database

        Parameters
        ----------
        entityClass : BaseEntity
            Entity class
        objs : list[dict]
            A list of objects

        Returns
        -------
        codes : list[str]
            List of code that have been putted to the database
        """
        # Loop through each object and put into the database
        codes = []
        try:
            self.__openSession()
            for obj in objs:
                entity = entityClass(**obj)
                entity.__table__.create(bind=self.engine, checkfirst=True)

                existed = self.session.query(entity.__class__) \
                    .filter(entity.__class__.Code == entity.Code) \
                    .first()
                if existed is None:
                    # Insert if entity is not exists
                    self.session.add(entity)
                else:
                    # Update if entity is exists
                    existed.copyFrom(entity)

                codes.append(entity.Code)
            # Commit all changes
            self.session.commit()
        finally:
            self.__closeSession()
        return codes

    def get(self, entityClass: BaseEntity, filterSpec=[], sortSpec=[], pagingSpec={}, joinClass=None) -> tuple[list, int]:
        """
        Get a list of entities from the database

        Parameters
        ----------
        entityClass : BaseEntity
            Entity class
        filterSpec : list[dict]
            List of conditions for filtering data
                Example:
                    [
                        {
                            'model': 'Workspace',
                            'field': 'Code',
                            'op': '==',
                            'value': '12345678'
                        },
                        {
                            'model': 'Project',
                            'field': 'Name',
                            'op': 'is_not_null'
                        }
                    ]
        sortSpec : list[dict]
            List of sort specs for sorting data
                Example:
                    [
                        {
                            'model': 'Workspace',
                            'field': 'Name',
                            'direction': 'asc'
                        },
                        {
                            'model': 'Project',
                            'field': 'Name',
                            'direction': 'desc'
                        }
                    ]
        pagingSpec : dict
            Using for pagination
                Example:
                    {
                        'pageNumber': 0,
                        'pageSize': 10
                    }

        joinClass : BaseEntity
            Using for join between two tables

        Returns
        -------
        entities : list[BaseEntity]
            List of entity from the database
        totalResults : int
            Total of the results
        """
        entities = []
        totalResults = 0
        try:
            self.__openSession()

            # Build dynamic query
            query = self.session.query(entityClass)

            # Append entity join
            if joinClass is not None:
                query = query.join(joinClass)

            # Build filter query
            query = apply_filters(query, filterSpec)

            # Build sort query
            query = apply_sort(query, sortSpec)

            # Build pagination query
            pageNumber = pagingSpec['pageNumber'] if 'pageNumber' in pagingSpec else None
            pageSize = pagingSpec['pageSize'] if 'pageSize' in pagingSpec else None

            query, pagination = apply_pagination(query,
                                                 page_number=pageNumber,
                                                 page_size=pageSize)
            totalResults = pagination[3]

            # Execute query
            entities = query.all()
        finally:
            self.__closeSession()
        return entities, totalResults

    def getOne(self, entityClass: BaseEntity, filterSpec=[], sortSpec=[]):
        """
        Get an entity from the database

        Parameters
        ----------
        entityClass : BaseEntity
            Entity class
        filterSpec : list[dict]
            List of conditions for filtering data
                Example:
                    [
                        {
                            'model': 'Workspace',
                            'field': 'Code',
                            'op': '==',
                            'value': '12345678'
                        },
                        {
                            'model': 'Project',
                            'field': 'Name',
                            'op': 'is_not_null'
                        }
                    ]
        sortSpec : list[dict]
            List of sort specs for sorting data
                Example:
                    [
                        {
                            'model': 'Workspace',
                            'field': 'Name',
                            'direction': 'asc'
                        },
                        {
                            'model': 'Project',
                            'field': 'Name',
                            'direction': 'desc'
                        }
                    ]

        Returns
        -------
        entity : BaseEntity
            An entity from the database
        """
        entity = None
        try:
            self.__openSession()

            # Build dynamic query
            query = self.session.query(entityClass)

            # Build filter query
            query = apply_filters(query, filterSpec)

            # Build sort query
            query = apply_sort(query, sortSpec)

            # Execute query
            entity = query.first()
        except Exception as error:
            entity = None
            Logger.instance().error(str(error))
        finally:
            self.__closeSession()
        return entity

    def checkExists(self, entityClass: BaseEntity, filterSpec=[], sortSpec=[]):
        """
        Check an entity exists in the database

        Parameters
        ----------
        entityClass : BaseEntity
            Entity class
        filterSpec : list[dict]
            List of conditions for filtering data
                Example:
                    [
                        {
                            'model': 'Workspace',
                            'field': 'Code',
                            'op': '==',
                            'value': '12345678'
                        },
                        {
                            'model': 'Project',
                            'field': 'Name',
                            'op': 'is_not_null'
                        }
                    ]
        sortSpec : list[dict]
            List of sort specs for sorting data
                Example:
                    [
                        {
                            'model': 'Workspace',
                            'field': 'Name',
                            'direction': 'asc'
                        },
                        {
                            'model': 'Project',
                            'field': 'Name',
                            'direction': 'desc'
                        }
                    ]

        Returns
        -------
        exists : bool
            Exists / Not exists in the database
        """
        exists = False
        try:
            self.__openSession()

            # Build dynamic query
            query = self.session.query(entityClass)

            # Build filter query
            query = apply_filters(query, filterSpec)

            # Build sort query
            query = apply_sort(query, sortSpec)

            # Execute query
            exists = query.first() is not None
        except Exception as error:
            exists = False
            Logger.instance().error(str(error))
        finally:
            self.__closeSession()
        return exists

    def delete(self, entityClass: BaseEntity, code: str) -> bool:
        """
        Delete a record in the database by Code

        Parameters
        ----------
        entityClass : BaseEntity
            Entity class
        code : str

        Returns
        -------
        success : bool
            Result of deleting a record
        """
        success = False
        try:
            self.__openSession()
            # Delete an entity by code
            entity = self.session.query(entityClass) \
                .filter(entityClass.Code == code) \
                .first()

            # Raise an exceotion when code is not exists
            if entity is None:
                raise InternalError(ERROR_DATABASE_0001)

            self.session.delete(entity)
            self.session.commit()
            success = True
        finally:
            self.__closeSession()
        return success

    def execute(self, query: str, **params):
        """
        Execute raw SQL string

        Parameters
        ----------
        query : str
            Raw SQL string
        params : 
            Parameters for raw SQL string

        Returns
        -------
        result : Any
            Result of execution
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(query), **params)
        return result
