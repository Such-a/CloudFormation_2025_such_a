from cfnlint.rules import CloudFormationLintRule, RuleMatch

class EC2VolumeTagRule(CloudFormationLintRule):
    """Check tags for EC2 Instances and Volumes"""

    id = "E9001"
    shortdesc = "Validate EC2 Instance and Volume tags"
    description = (
        "Ensure EC2 t2.micro instances have FreeTierEligible=true, "
        "m5.large instances have PerformanceCritical=true/false, "
        "and gp3 volumes have Priority between 3000–16000."
    )
    tags = ["ec2", "ebs", "tags", "custom"]

    defaults = {
        "t2_micro_tag": "FreeTierEligible",
        "m5_large_tag": "PerformanceCritical",
        "gp3_tag": "Priority",
        "gp3_range": [3000, 16000],
        "m5_values": ["true", "false"],
        "t2_values": ["true"],
    }

    def __init__(self):
        super().__init__()

    def check_tag(self, resource_name, resource, tag_key, valid_values=None, numeric_range=None):
        """Helper to check if tag exists and is valid"""
        tags = resource.get("Properties", {}).get("Tags", [])
        matches = []

        if not isinstance(tags, list):
            matches.append(RuleMatch(
                ["Resources", resource_name, "Properties", "Tags"],
                f"Tags should be a list in {resource_name}"
            ))
            return matches

        found = next((t for t in tags if t.get("Key") == tag_key), None)
        if not found:
            matches.append(RuleMatch(
                ["Resources", resource_name, "Properties", "Tags"],
                f"Missing required tag '{tag_key}' in {resource_name}"
            ))
        else:
            value = found.get("Value")
            if valid_values and value not in valid_values:
                matches.append(RuleMatch(
                    ["Resources", resource_name, "Properties", "Tags", tag_key],
                    f"Invalid value '{value}' for tag '{tag_key}'. Expected one of {valid_values}."
                ))
            if numeric_range:
                try:
                    val_int = int(value)
                    if not (numeric_range[0] <= val_int <= numeric_range[1]):
                        matches.append(RuleMatch(
                            ["Resources", resource_name, "Properties", "Tags", tag_key],
                            f"Tag '{tag_key}' value {value} must be between {numeric_range[0]} and {numeric_range[1]}."
                        ))
                except (ValueError, TypeError):
                    matches.append(RuleMatch(
                        ["Resources", resource_name, "Properties", "Tags", tag_key],
                        f"Tag '{tag_key}' value must be numeric."
                    ))
        return matches

    def match(self, cfn):
        matches = []
        resources = cfn.get_resources()

        for name, resource in resources.items():
            rtype = resource.get("Type")

            if rtype == "AWS::EC2::Instance":
                instance_type = resource.get("Properties", {}).get("InstanceType")
                if instance_type == "t2.micro":
                    matches.extend(self.check_tag(
                        name, resource,
                        self.defaults["t2_micro_tag"],
                        valid_values=self.defaults["t2_values"]
                    ))
                elif instance_type == "m5.large":
                    matches.extend(self.check_tag(
                        name, resource,
                        self.defaults["m5_large_tag"],
                        valid_values=self.defaults["m5_values"]
                    ))

            elif rtype == "AWS::EC2::Volume":
                volume_type = resource.get("Properties", {}).get("VolumeType")
                if volume_type == "gp3":
                    matches.extend(self.check_tag(
                        name, resource,
                        self.defaults["gp3_tag"],
                        numeric_range=self.defaults["gp3_range"]
                    ))

        return matches


class S3PublicAccessTagRule(CloudFormationLintRule):
    """Check tags for S3 Buckets with PublicAccessBlockConfiguration"""

    id = "E9002"
    shortdesc = "Validate S3 bucket tags when public access is allowed"
    description = (
        "If any PublicAccessBlockConfiguration parameter is false, "
        "the bucket must have the tag PublicAccessAllowed=true."
    )
    tags = ["s3", "tags", "custom"]

    defaults = {
        "s3_tag": "PublicAccessAllowed",
        "s3_value": ["true"]
    }

    def __init__(self):
        super().__init__()

    def check_tag(self, resource_name, resource, tag_key, valid_values=None):
        tags = resource.get("Properties", {}).get("Tags", [])
        matches = []

        if not isinstance(tags, list):
            matches.append(RuleMatch(
                ["Resources", resource_name, "Properties", "Tags"],
                f"Tags should be a list in {resource_name}"
            ))
            return matches

        found = next((t for t in tags if t.get("Key") == tag_key), None)
        if not found:
            matches.append(RuleMatch(
                ["Resources", resource_name, "Properties", "Tags"],
                f"Missing required tag '{tag_key}' in {resource_name}"
            ))
        else:
            value = found.get("Value")
            if valid_values and value not in valid_values:
                matches.append(RuleMatch(
                    ["Resources", resource_name, "Properties", "Tags", tag_key],
                    f"Invalid value '{value}' for tag '{tag_key}'. Expected one of {valid_values}."
                ))
        return matches

    def match(self, cfn):
        matches = []
        resources = cfn.get_resources()

        for name, resource in resources.items():
            if resource.get("Type") == "AWS::S3::Bucket":
                pab = resource.get("Properties", {}).get("PublicAccessBlockConfiguration")
                if pab and isinstance(pab, dict):
                    if any(val is False for val in pab.values()):
                        matches.extend(self.check_tag(
                            name, resource,
                            self.defaults["s3_tag"],
                            valid_values=self.defaults["s3_value"]
                        ))
        return matches
