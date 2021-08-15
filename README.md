# CloudFormation Guard Rules

> A collection of CloudFormation Guard 2.0 rules

## Usage

To use the rules against your CloudFormation template:

```
cfn-guard validate -r rules/ -s -d mytemplate.yaml
```

## Testing

To run the unit tests:

```
find rules -name "*.guard" -print0 | xargs -0 -n1 cfn-guard test -t tests/ -r
```
