from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    STAFF = "staff"
    ADMIN = "admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class TicketStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class TicketCategory(str, Enum):
    PRODUCT_INFORMATION = "product_information"
    PRICING = "pricing"
    DEMO_REQUEST = "demo_request"
    TECHNICAL_SUPPORT = "technical_support"
    SERVICE_FEEDBACK = "service_feedback"
    COMPLAINT = "complaint"
    OTHER = "other"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class TicketEventType(str, Enum):
    CREATED = "created"
    ANALYZED = "analyzed"    #AI-analyzed
    ASSIGNED = "assigned"
    STATUS_CHANGED = "status_changed"
    CATEGORY_CHANGED = "category_changed"
    PRIORITY_CHANGED = "priority_changed"
    MESSAGE_SENT = "message_sent"