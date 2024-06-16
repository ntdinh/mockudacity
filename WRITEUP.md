# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*For **both** a VM or App Service solution for the CMS app:*
- *Analyze costs, scalability, availability, and workflow*
- *Choose the appropriate solution (VM or App Service) for deploying the app*
- *Justify your choice*

Costs:
VM: Can be cost-effective for workloads that need full control over resources and can be optimized by choosing specific VM sizes or using reserved instances.
App Service: Typically offers a more predictable pricing model based on the App Service plan. Reduced management overhead can lead to lower operational costs.

Scalability:
VM: Can scale vertically (by resizing the VM) or horizontally (by adding more VMs), but manual configuration is required.
App Service: Supports automatic scaling (both horizontal and vertical) based on demand without additional configuration. It’s easier to adjust the scale in response to traffic changes.
### Assess app changes that would change your decision.

I chose App Services because:
- Supports multiple languages and frameworks out-of-the-box, like .NET, Java, Node.js, Python, and PHP. Quick to start development without worrying about environment setup.
- Can be cost-effective for workloads that need full control over resources and can be optimized by choosing specific VM sizes or using reserved instances.
- Web applications, APIs, and mobile backends needing a quick deployment, easy management, and scalable platform with minimal operational overhead.