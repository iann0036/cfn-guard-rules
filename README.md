# CloudFormation Guard Rules

> A collection of CloudFormation Guard 2.0 rules

## Usage

To use the rules against your CloudFormation template:

```
cfn-guard validate -r rules/ -d mytemplate.yaml -s
```

## Testing

To run the unit tests:

```
cfn-guard test -r rules/efs.guard -t tests/efs.yaml
cfn-guard test -r rules/iam.guard -t tests/iam.yaml
...
```
