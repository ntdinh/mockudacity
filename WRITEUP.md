# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*For **both** a VM or App Service solution for the CMS app:*
- *Analyze costs, scalability, availability, and workflow*
- *Choose the appropriate solution (VM or App Service) for deploying the app*

Costs:
VM: Can be cost-effective for workloads that need full control over resources and can be optimized by choosing specific VM sizes or using reserved instances.
App Service: Typically offers a more predictable pricing model based on the App Service plan. Reduced management overhead can lead to lower operational costs.

Scalability:
VM: Can scale vertically (by resizing the VM) or horizontally (by adding more VMs), but manual configuration is required.
App Service: Supports automatic scaling (both horizontal and vertical) based on demand without additional configuration. It’s easier to adjust the scale in response to traffic changes.

Workflow:
VM:
    - Pipeline: Custom CI/CD pipelines are needed for building, deploying, and configuring the application.
    - Customization: Offers high flexibility in deployment methods and environments
    - The developer has complete control over the environment by configuring the server and is responsible for updating the operating system, applying patches, and managing the virtual machine overall
App Service:
    - Pipeline: Built-in CI/CD integration simplifies the deployment process.
    - Customization: Less flexibility compared to VMs but streamlined and efficient for supported languages and frameworks.
    - Limited control because it have to go under infrastructure and the service will handle OS updates, patches...

Availability: 
VM: Requires custom setup for high availability, fault tolerance, and disaster recovery, offering high flexibility but also increased complexity and management.
App Service: Delivers built-in high availability and disaster recovery features with minimal configuration, simplifying the process but with less control over specific aspects compared to VMs.

### Assess app changes that would change your decision.

- I will reconsider my decision when moving an application from an on-premises environment to the cloud.
- When I need specific configurations, such as non-standard software or extensive network setups.
- Additionally, when dealing with resource-demanding workloads like running complex databases or engaging in high-performance computing.