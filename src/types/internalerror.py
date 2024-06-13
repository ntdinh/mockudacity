class InternalError(Exception):
    def __init__(self, error, *args: object) -> None:
        super().__init__(*args)
        self.Code = error['Code']
        self.Msg = error['Msg']
