
from typing import Optional, Set
from enum import Enum, unique

from . import base, submodel


@unique
class PermissionKind(Enum):
    """
    Description of the kind of permission. Possible kind of permission also include the denial of the permission.

    Comment for devs: I found the enum members to be typically written in all caps, but couldn't verify this

    ALLOW: Allow the permission given to the subject
    DENY: Explicitly deny the permission given to the subject
    NOT_APPLICABLE: The permission is not applicable to the subject
    UNDEFINED: It is undefined whether the permission is allowed, not applicable or denied to the subject
    """
    ALLOW = 0
    DENY = 1
    NOT_APPLICABLE = 2
    UNDEFINED = 3


class Permission:
    """
    Description of a single permission

    :ivar permission: Reference to a property that defines the semantics of the permission
    :ivar kind_of_permission: Description of the kind of permission
    """
    def __init__(self,
                 permission: submodel.Property,
                 kind_of_permission: PermissionKind):
        """
        Initializer of Permission

        :param permission: Reference to a property that defines the semantics of the permission
        :param kind_of_permission: Description of the kind of permission
        """

        self.permission: submodel.Property = permission
        self.kind_of_permission: PermissionKind = kind_of_permission


class ObjectAttribute:
    """
    A set of data elements that describe object attributes. These attributes need to refer to a data element within an
    existing submodel.

    Comment for devs: This deviates from the paper, as in the paper, there is a list of Object Attributes as its own
    class. I changed it, so that the list is now in the PermissionsPerObject class, as a list of instances of
    this class, as otherwise I'd add an extra class "ObjectAttributes" which seems extra to me.

    :ivar object_attribute: A data elements that further classifies an object.
    """
    def __init__(self,
                 object_attribute: submodel.Property):
        """
        Initializer of ObjectAttribute

        :param object_attribute: A data elements that further classifies an object.
        """

        self.object_attribute: submodel.Property = object_attribute


class PermissionsPerObject:
    """
    Defines access permissions for a specified object.

    The object is any referable element in the AAS. Additionally object attributes can be defined that further specify
    the kind of object the permissions apply to.

    :ivar permission_object: Element to which permission shall be assigned
    :ivar target_object_attribute: Target object attributes that need to be fulfilled so that the access permissions
                                   apply to the accessing subject.
    :ivar permissions: Permissions assigned to the object. The permissions hold for all subjects as specified in the
                       access permission rule.
    """
    def __init__(self,
                 permission_object: base.Referable,
                 target_object_attribute: Set[ObjectAttribute],
                 permissions: Set[Permission]):
        """
        Initializer of PermissionsPerObject

        :param permission_object: Element to which permission shall be assigned
        :param target_object_attribute: Target object attributes that need to be fulfilled so that the access permissions
                                        apply to the accessing subject.
        :param permissions: Permissions assigned to the object. The permissions hold for all subjects as specified in the
                            access permission rule.
        """

        self.permission_object: base.Referable = permission_object
        self.target_object_attribute: Set[ObjectAttribute] = target_object_attribute
        self.permissions: Set[Permission] = permissions


class SubjectAttribute:
    """
    A list of data elements that further classifies a specific subject

    :ivar subject_attribute: A data element that further classifies a specific subject.
    """
    def __init__(self,
                 subject_attribute: submodel.Property):
        """
        Initializer of SubjectAttribute

        :param subject_attribute: A data element that further classifies a specific subject.
        """

        self.subject_attribute: submodel.Property = subject_attribute


class AccessPermissionRule(base.Referable, base.Qualifiable):
    """
    Table that defines access permissions per authenticated subject for a set of objects (referable elements)

    :param target_subject_attribute: Unordered list of instances of the class SubjectAttribute Target subject
                                     attributes that need to be fulfilled by the accessing subject to get the
                                     permissions defined by this rule.
    :param permissions_per_object: Unordered list of instances of the class PermissionsPerObject Set of
                                   object-permission pairs that define the permissions per object within the
                                   access permission rule

    """
    def __init__(self,
                 id_short: str,
                 target_subject_attribute: Set[SubjectAttribute] = set(),
                 permissions_per_object: Set[PermissionsPerObject] = set(),
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.Reference] = None,
                 qualifier: Set[base.Constraint] = set()):
        """
        Initializer of AccessPermissionRule

        :param id_short: Identifying string of the element within its name space. (from base.Referable)
        :param target_subject_attribute: Unordered list of instances of the class SubjectAttribute Target subject
                                         attributes that need to be fulfilled by the accessing subject to get the
                                         permissions defined by this rule.
        :param permissions_per_object: Unordered list of instances of the class PermissionsPerObject Set of object-permission
                                       pairs that define the permissions per object within the access permission rule
        :param qualifier: Unordered list of Constraints that gives additional qualification of a qualifiable element.
                          (from base.Qualifiable)
        :param category: The category is a value that gives further meta information w.r.t. to the class of the element.
                         It affects the expected existence of attributes and the applicability of constraints.
                         (from base.Referable)
        :param description: Description or comments on the element. (from base.Referable)
        :param parent: Reference to the next referable parent element of the element. (from base.Referable)
        """

        super().__init__()
        self.id_short: str = id_short
        self.category: Optional[str] = category
        self.description: Optional[base.LangStringSet] = description
        self.parent: Optional[base.Reference] = parent
        self.qualifier: Set[base.Constraint] = qualifier
        self.target_subject_attribute: Set[SubjectAttribute] = target_subject_attribute
        self.permissions_per_object: Set[PermissionsPerObject] = permissions_per_object


class AccessControl:
    """
    Defines the local access control policy administration point, has the major task of defining the access permission
    rules.

    The policy decision point of access control as realized by the AAS itself

    :ivar selectable_subject_attributes: Reference to a submodel defining the authenticated subjects to access elements
                                         that are configured for the AAS. They are selectable by the access permission
                                         rules to assign permissions to the subjects.
                                          TODO: Default: refer to submodel of default_subject_attributes
    :ivar default_subject_attributes: Reference to a submodel defining the default subjects attributes for the AAS
                                      that can be used to describe access permission rules.
    :ivar selectable_permissions: Reference to a submodel defining which permissions can be assigned to the subjects
                                   TODO: Default: refer to submodel of default_permissions
    :ivar default_permissions: Reference to a submodel defining the default permissions for the AAS.
    :ivar selectable_environment_attributes: Reference to a submodel defining which environment attributes can be
                                             accessed via the permission rules defined for the AAS, i.e. attributes
                                             that are not describing the asset itself.
                                              TODO: Default refer to default_environment_attributes
    :ivar default_environment_attributes: Reference to a submodel defining default environment attributes, i.e.
                                          attributes that are not describing the asset itself.
    :ivar access_permission_rule: Unordered list of instances of the class AccessPermissionRule Access permission rules
                                  of the AAS describing the rights assigned to (already authenticated) subjects to
                                  access elements of the AAS
    """

    def __init__(self,
                 selectable_subject_attributes: submodel.Submodel,
                 default_subject_attributes: submodel.Submodel,
                 selectable_permissions: submodel.Submodel,
                 default_permissions: submodel.Submodel,
                 selectable_environment_attributes: submodel.Submodel,
                 default_environment_attributes: submodel.Submodel,
                 access_permission_rule: Set[AccessPermissionRule]):
        """
        Initializer of AccessControl

        :param selectable_subject_attributes: Reference to a submodel defining the authenticated subjects to access
                                              elements that are configured for the AAS. They are selectable by the
                                              access permission rules to assign permissions to the subjects.
                                          TODO: Default: refer to submodel of default_subject_attributes
        :param default_subject_attributes: Reference to a submodel defining the default subjects attributes for the AAS
                                           that can be used to describe access permission rules.
        :param selectable_permissions: Reference to a submodel defining which permissions can be assigned to the
                                       subjects
                                       TODO: Default: refer to submodel of default_permissions
        :param default_permissions: Reference to a submodel defining the default permissions for the AAS.
        :param selectable_environment_attributes: Reference to a submodel defining which environment attributes can be
                                                  accessed via the permission rules defined for the AAS, i.e. attributes
                                                  that are not describing the asset itself.
                                                  TODO: Default refer to default_environment_attributes
        :param default_environment_attributes: Reference to a submodel defining default environment attributes, i.e.
                                               attributes that are not describing the asset itself.
        :param access_permission_rule: Unordered list of instances of the class AccessPermissionRule Access permission
                                        rules of the AAS describing the rights assigned to (already authenticated)
                                        subjects to access elements of the AAS
        """

        self.selectable_subject_attributes: submodel.Submodel = selectable_subject_attributes
        self.default_subject_attributes: submodel.Submodel = default_subject_attributes
        self.selectable_permissions: submodel.Submodel = selectable_permissions
        self.default_permissions: submodel.Submodel = default_permissions
        self.selectable_environment_attributes: submodel.Submodel = selectable_environment_attributes
        self.default_environment_attributes: submodel.Submodel = default_environment_attributes
        self.access_permission_rule: Set[AccessPermissionRule] = access_permission_rule


class Endpoint:
    """
    Endpoint to an external access control defining a policy administration point to be used by the AAS

    not yet specified in the current Metamodel
    """
    pass


class PolicyAdministrationPoint:
    """
    Definition of a security administration point (PDP)

    :ivar access_control: Instance of Access Control
    :ivar endpoint: Instance of Endpoint
    """
    def __init__(self,
                 access_control: Optional[AccessControl]  = None,
                 endpoint: Optional[Endpoint] = None):
        """
        Initializer of PolicyAdministrationPoint

        :param access_control: Instance of Access Control (optional)
        :param endpoint: Instance of Endpoint (optional)
        """

        self.local_access_control: Optional[AccessControl] = access_control
        self.external_access_control: Optional[Endpoint] = endpoint


class PolicyDecisionPoint:
    """
    Computes access decisions by evaluating the applicable Digital Policies and Meta-Policies. One of the main functions
    of the PDP is to mediate or de-conflict Digital Policies according to Meta-Policies
    TODO: Find definition from [22]
    """
    pass


class PolicyEnforcementPoint:
    """
    TODO: Find anything about this class

    """
    pass


class PolicyInformationPoints:
    """
    Defines the security policy information points (PIP)

    Serves as the retrieval attributes, or the data required for policy evaluation to provide the information needed
    by the policy decision point to make the decisions.

    :param external_information_point: Unordered list of endpoints to external available information points taking into
                                       consideration for access control for the AAS
    :param internal_information_point: Unordered list of references to submodels defining information used by security
                                       access permission rules
    """
    def __init__(self,
                 external_information_point: Set[Endpoint] = set(),
                 internal_information_point: Set[submodel.Submodel] = set()):
        """
        Initializer of PolicyInformationPoints

        :param external_information_point: Unordered list of endpoints to external available information points taking
                                           into consideration for access control for the AAS
        :param internal_information_point: Unordered list of references to submodels defining information used by
                                           security access permission rules
        """
        self.external_information_point: Set[Endpoint] = external_information_point
        self.internal_information_point: Set[submodel.Submodel] = internal_information_point


class AccessControlPolicyPoints:
    """
    Container for access control policy points

    :ivar policy_administration_point: Instance of PolicyAdministrationPoint
    :ivar policy_decision_point: Instance of PolicyDecisionPoint
    :ivar policy_enforcement_point: Instance of PolicyEnforcementPoint
    :ivar policy_information_points: Instance of PolicyInformationPoints
    """
    def __init__(self,
                 policy_administration_point: PolicyAdministrationPoint,
                 policy_decision_point: PolicyDecisionPoint,
                 policy_enforcement_point: PolicyEnforcementPoint,
                 policy_information_points: Optional[PolicyInformationPoints] = None):
        """
        Initializer of AccessControlPolicyPoints

        :param policy_administration_point: Instance of PolicyAdministrationPoint
        :param policy_decision_point: Instance of PolicyDecisionPoint
        :param policy_enforcement_point: Instance of PolicyEnforcementPoint
        :param policy_information_points: Instance of PolicyInformationPoints
        """

        self.policy_administration_point: PolicyAdministrationPoint = policy_administration_point
        self.policy_decision_point: PolicyDecisionPoint = policy_decision_point
        self.policy_enforcement_point: PolicyEnforcementPoint = policy_enforcement_point
        self.policy_information_points: Optional[PolicyInformationPoints] = policy_information_points


class Certificate:
    """
    Certificate is not yet further defined
    """
    pass


class Security:
    """
    Container for security relevant information of the AAS.

    :ivar access_control_policy_point: Instance of the PolicyAdministrationPoint Class
    :ivar trust_anchor: Unordered list of used certificates
    """
    def __init__(self,
                 access_control_policy_point: AccessControlPolicyPoints,
                 trust_anchor: Set[Certificate] = set()):
        """
        Initializer of Security

        :param access_control_policy_point: Instance of the PolicyAdministrationPoint Class
        :param trust_anchor: Unordered list of used certificates
        """

        self.access_control_policy_point: AccessControlPolicyPoints = access_control_policy_point
        self.trust_anchor: Set[Certificate] = trust_anchor
