# ExDEX Website Structure

This directory hosts the deployment skeleton for the ExDEX website. It contains Docker and configuration files used to run a development instance.

The folder was previously named `stucture`; update any build scripts or deployment configurations to reference `website/structure` instead.

Two copies of the site are included here:

1. The files in this directory for active development.
2. `PROXGUARD.WEBSITE_.zip`, an archived copy of the original site that can be extracted for quick setup or backup.

When deploying the site, ensure the backend node exposes the smart contract interfaces. These endpoints will be available through your XDEX dashboard.
Note that the smart contract source files themselves are not stored here. Obtain the official ExDEX contracts and place them in a `contracts/` directory before deployment.
