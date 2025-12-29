
CREATE TABLE "user" (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE workspace (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id)
);

CREATE TABLE workspace_has_user (
    workspace_id UUID NOT NULL,
    user_id UUID NOT NULL,

    PRIMARY KEY (workspace_id, user_id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE TABLE task_type (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,
    parent_type_id UUID NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id),
    FOREIGN KEY (parent_type_id) REFERENCES task_type(id)
);

CREATE TABLE team (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id)
);

CREATE TABLE team_has_user (
    team_id UUID NOT NULL,
    user_id UUID NOT NULL,

    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES team(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE TABLE feedback (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,

    description TEXT NULL,
    feedback_type VARCHAR(100) NOT NULL,
    user_from UUID NOT NULL,
    user_to UUID NOT NULL,
    delivered BOOLEAN NOT NULL DEFAULT FALSE,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id),

    FOREIGN KEY (user_from) REFERENCES "user"(id),
    FOREIGN KEY (user_to) REFERENCES "user"(id)
);

CREATE TABLE goal (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,

    status VARCHAR(100) NOT NULL,
    description TEXT NULL,
    feedback_type VARCHAR(100) NOT NULL,
    due_date TIMESTAMP NOT NULL,
    user_id UUID NULL,
    team_id UUID NULL,
    parent_goal_id UUID NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id),
    FOREIGN KEY (user_id) REFERENCES "user"(id),
    FOREIGN KEY (team_id) REFERENCES team(id),
    FOREIGN KEY (parent_goal_id) REFERENCES goal(id)
);

CREATE TABLE meeting (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,

    meeting_date TIMESTAMP NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id)
);

CREATE TABLE meeting_has_user (
    meeting_id UUID NOT NULL,
    user_id UUID NOT NULL,

    PRIMARY KEY (meeting_id, user_id),
    FOREIGN KEY (meeting_id) REFERENCES meeting(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE TABLE meeting_note (
    id UUID NOT NULL,
    meeting_id UUID NOT NULL,
    note TEXT NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (meeting_id) REFERENCES meeting(id) ON DELETE CASCADE
);
