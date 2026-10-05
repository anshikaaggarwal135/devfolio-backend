from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    technologies = db.Column(db.String(500))
    github_url = db.Column(db.String(500))
    live_url = db.Column(db.String(500))

    # CMS-manageable project image
    image_url = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))

    icon_url = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    technologies = db.Column(db.String(500))

    company_logo_url = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.Integer, primary_key=True)

    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(150), nullable=False)

    field_of_study = db.Column(db.String(150))

    description = db.Column(db.Text)

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    institution_logo_url = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class Certification(db.Model):
    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    issue_date = db.Column(db.Date)

    credential_url = db.Column(db.String(500))

    certificate_image_url = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    subject = db.Column(db.String(200))

    message = db.Column(db.Text, nullable=False)

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class About(db.Model):
    __tablename__ = "about"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(150),
        nullable=False,
        default="About Me"
    )

    content = db.Column(db.Text, nullable=False)

    profile_image_url = db.Column(db.String(500))

    resume_url = db.Column(db.String(500))

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )
class Hero(db.Model):
    __tablename__ = "hero"

    id = db.Column(db.Integer, primary_key=True)

    greeting = db.Column(
        db.String(150),
        default="Hi, I'm"
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    subtitle = db.Column(db.Text)

    profile_image_url = db.Column(db.String(500))

    primary_button_text = db.Column(
        db.String(100),
        default="View Projects"
    )

    primary_button_url = db.Column(
        db.String(500)
    )

    secondary_button_text = db.Column(
        db.String(100),
        default="Contact Me"
    )

    secondary_button_url = db.Column(
        db.String(500)
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )
class SocialLink(db.Model):
    __tablename__ = "social_links"

    id = db.Column(db.Integer, primary_key=True)

    platform = db.Column(
        db.String(100),
        nullable=False
    )

    url = db.Column(
        db.String(500),
        nullable=False
    )

    icon_url = db.Column(
        db.String(500)
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    display_order = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class SiteSetting(db.Model):
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)

    site_name = db.Column(
        db.String(150),
        nullable=False,
        default="Devfolio"
    )

    email = db.Column(
        db.String(150)
    )

    phone = db.Column(
        db.String(50)
    )

    location = db.Column(
        db.String(200)
    )

    favicon_url = db.Column(
        db.String(500)
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )