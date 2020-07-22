## marapp-workers
 
AWS Lambda workers for Marapp.

## Installation

```bash
$ make setup
```

A virtualenv will automatically be created, and packages from the [Pipfile](./Pipfile) installed.

## Running

Activate the virtualenv.

```bash
$ pipenv shell
```

To kill the virtualenv.

```bash
$ pipenv deactivate
```

The following environment variables are required by the service.

| **Key**                | **Description**                                                                      |
| ---------------------- |------------------------------------------------------------------------------------- |
| GOOGLE_SERVICE_ACCOUNT | GCP Service Account Private Key.                                                     |
| SERVICE_API_ENDPOINT   | API endpoint for [marapp-services](https://github.com/natgeosociety/marapp-services).|
| SERVICE_API_KEY        | API secret for [marapp-services](https://github.com/natgeosociety/marapp-services).  |
| SNS_RESULT_TOPIC_ARN   | Topic ARN from [marapp-services](https://github.com/natgeosociety/marapp-services).  |
| SENTRY_DSN             | (optional) Sentry DSN Key.                                                           |

The required environment variables are also described in [.env.sample](.env.sample).

####  VPC Configuration

You can configure the functions to connect to private subnets in a virtual private cloud (VPC) in your account.

The following environment variables are required to connect to a VPC.
```shell script
VPC_SECURITY_GROUP_ID_1='<SECURITY-GROUP-ID1>'
VPC_SECURITY_GROUP_ID_2='<SECURITY-GROUP-ID2>'
...
VPC_SUBNET_ID_1='<SUBNET_ID1>'
VPC_SUBNET_ID_2='<SUBNET_ID2>'
...
```
For more details, see: https://www.serverless.com/framework/docs/providers/aws/guide/functions#vpc-configuration

## Packaging & deployment

Installs Serverless Framework and dependencies.

```bash
npm install
```

Create & deploy all required services. 

You will need an AWS access key ID and secret pair stored in `~/.aws/credentials`.

Alternatively, you can authenticate via the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.

You will need to have access to the following AWS services:
- CloudFormation

Create a local `.env` file based on [.env.sample](.env.sample), add the required configuration for the environment, and run:

```shell script
npm run serverless:deploy -- --stage <env>
```

Use the `--force` flag when your previous deployment failed.

## Configure Earth Engine assets

The template from [earthengine.yaml](src/earthengine.yaml) is required to map existing [Google Earth Engine](https://earthengine.google.com) image assets to computations supported by the library.

For more details about managing assets in Earth Engine, see: https://developers.google.com/earth-engine/asset_manager

The following public assets serve as examples for different types of computations supported by the [marapp-metrics](https://github.com/natgeosociety/marapp-metrics) library.

| **Type** | **Dataset** |
| ------------- |---------------- |
| `biodiversity_intactness` | https://data.nhm.ac.uk/dataset/global-map-of-the-biodiversity-intactness-index-from-newbold-et-al-2016-science |
| `human_footprint` | https://datadryad.org/stash/dataset/doi:10.5061/dryad.052q5 |
| `human_impact` | http://hdr.undp.org/en/content/human-development-index-hdi |
| `land_cover` | http://maps.elie.ucl.ac.be/CCI/viewer/ |
| `modis_evi` | https://lpdaac.usgs.gov/products/mod13q1v006/ |
| `modis_fire`|  http://modis-fire.umd.edu/ |
| `protected_areas` | https://www.protectedplanet.net/ |
| `terrestrial_carbon` | https://developers.google.com/earth-engine/datasets/catalog/WCMC_biomass_carbon_density_v1_0 |
| `tree_loss` | https://earthenginepartners.appspot.com/science-2013-global-forest/download_v1.5.html |
