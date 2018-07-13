DRAFT_STAGE = 0
ACTIVE_STAGE = 1
DEAD_STAGE = 2
COMPLETED_STAGE = 3
EXPIRED_STAGE = 4

STAGE_CHOICES = (
    (DRAFT_STAGE, 'Draft'),
    (ACTIVE_STAGE, 'Active'),
    (DEAD_STAGE, 'Dead'),
    (COMPLETED_STAGE, 'Completed'),
    (EXPIRED_STAGE, 'Expired'),
)

BEGINNER = 0
INTERMEDIATE = 1
ADVANCED = 2

DIFFICULTY_CHOICES = (
    (BEGINNER, 'Beginner'),
    (INTERMEDIATE, 'Intermediate'),
    (ADVANCED, 'Advanced'),
)

rev_mapped_difficulties =  dict((y, x) for x, y in DIFFICULTY_CHOICES)
