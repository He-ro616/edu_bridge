from .database import db
from datetime import datetime
from flask_login import UserMixin
#from werkzeug.security import generate_password_hash


# # Association Table: User ↔ Mentor
# user_mentor_association = db.Table(
#     'user_mentor_association',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('mentor_id', db.Integer, db.ForeignKey('mentor.id'))
# )

# # Association Table: Mentor ↔ Course
# mentor_course_association = db.Table(
#     'mentor_course_association',
#     db.Column('mentor_id', db.Integer, db.ForeignKey('mentor.id')),
#     db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
# )

# Association table for Progress-Badge many-to-many relationship
progress_badges = db.Table('progress_badges',
    db.Column('progress_id', db.Integer, db.ForeignKey('progress.id'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('badges.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    fullname = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    qualification = db.Column(db.String(200), nullable = False)
    language_pref = db.Column(db.String(200), nullable = False)
    interest = db.Column(db.String(200), nullable = False)
    date_of_birth = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')

    # #Relationship
    # progress = db.relationship('Progress', back_populates='user', lazy='dynamic')
    # messages_sent = db.relationship('Message', backref='sender', lazy='dynamic', foreign_keys='Message.sender_id')
    # notes = db.relationship('Note', backref='uploader', lazy='dynamic')
    # quizzes_created_as_admin = db.relationship('Quiz', foreign_keys='Quiz.created_by_user_id', lazy='dynamic')
    # Relationships
    progress_entries = db.relationship('Progress', back_populates='user', lazy='dynamic')  # Renamed
    messages_sent = db.relationship('Message', backref='sender', lazy='dynamic', foreign_keys='Message.sender_id')
    notes = db.relationship('Note', backref='uploader', lazy='dynamic')
    quizzes_created_as_admin = db.relationship('Quiz', foreign_keys='Quiz.created_by_user_id', backref='admin_creator', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}>"
    
    # def get_id(self):
    #     return f"user:{self.id}"
    # def role(self):
    #     return self.role  # or 'student', depending on your logic

    
    
    # def __init__(self, username, fullname, email, password, qualification, dob):
    #     self.username = username
    #     self.fullname = fullname
    #     self.email = email
    #     #self.password = generate_password_hash(password)
    #     self.qualification = qualification
    #     self.dob = dob
    #     self.is_active = True  



class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable = False)
    language = db.Column(db.String(10), default='en')
    level = db.Column(db.String(50), nullable=False)
    # Relationships
    modules = db.relationship('Module', backref='course_modules', lazy='subquery', cascade="all, delete-orphan")
    quizzes = db.relationship('Quiz', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    # progress = db.relationship('Progress', back_populates='course', lazy='dynamic')
    progress = db.relationship('Progress', back_populates='course', lazy='dynamic')
    notes = db.relationship('Note', backref='course', lazy='dynamic',cascade='all, delete-orphan')
    quiz_attempts = db.relationship("QuizAttempt", back_populates="course", lazy="dynamic")
    # mentors = db.relationship('Mentor', secondary=mentor_course_association, back_populates='courses')

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    video_path = db.Column(db.String(200))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    #course = db.relationship('Course', back_populates='modules')
    submodules = db.relationship('SubModule', backref='module', cascade='all, delete-orphan')

class SubModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    video_path = db.Column(db.String(200))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    #module = db.relationship('Module', backref='submodules')  # Ensure relationship with module


class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=True)  # Null for assignments
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)  # Score out of 100
    completion_percentage = db.Column(db.Float, default=0.0)  # % of course completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # # Relationships
    # user = db.relationship('User', backref='progress', lazy='dynamic')
    # quiz = db.relationship('Quiz', backref='progress')
    # course = db.relationship('Course', backref='progress_records', lazy='dynamic')
    # badges = db.relationship('Badge', secondary='progress_badges', backref='progress')
    # quiz_attempt = db.relationship('QuizAttempt', backref='progress_entry', uselist=False)  # Updated backref name

   # Relationships
    user = db.relationship('User', back_populates='progress_entries', lazy='select')  # Changed to lazy='select'
    # course = db.relationship('Course', back_populates='progress_records', lazy='select')    # Changed to lazy='select'
    course = db.relationship('Course', back_populates='progress', lazy='select')  # Use 'progress' here to align with Course model
    quiz_attempts = db.relationship('QuizAttempt', backref='progress_record', lazy='dynamic')

    def __repr__(self):
        return f'<Progress user_id={self.user_id} course_id={self.course_id} completion={self.completion_percentage}>'

class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Quiz Master"
    description = db.Column(db.String(200), nullable=False)  # e.g., "Scored 80%+ in a quiz"
    icon_url = db.Column(db.String(200), nullable=True)  # URL to badge icon
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Badge name={self.name}>'

class Mentor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    expertise = db.Column(db.String(200))
    availability = db.Column(db.String(80), default=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80),nullable=False)
    language_pref = db.Column(db.String(80),nullable=False)
    role = db.Column(db.String(80), default='mentor')
    #role=db.Column(db.String(50), default='mentor')
    # Relationships
    # courses = db.relationship('Course', secondary=mentor_course_association, back_populates='mentors')
    messages_received = db.relationship('Message', backref='receiver', lazy='dynamic', foreign_keys='Message.receiver_id')
    quizzes_created_as_mentor = db.relationship('Quiz', foreign_keys='Quiz.created_by_mentor_id', lazy='dynamic')

    notes_uploaded = db.relationship('Note', backref='mentor_uploader', lazy='dynamic')
    # students = db.relationship('User', secondary=user_mentor_association, back_populates='mentors')
    # @property
    # def role(self):
    #     return self.role
    def get_id(self):
        # Ensure get_id returns a string, not a set
        return str(self.id)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    time_limit = db.Column(db.Integer, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by_mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #user_creator = db.relationship('User', foreign_keys=[created_by_user_id])
    #mentor_creator = db.relationship('Mentor', foreign_keys=[created_by_mentor_id])

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    # attempts = db.relationship('QuizAttempt', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', back_populates='quiz')


    __table_args__ = (
        db.CheckConstraint(
            '(created_by_user_id IS NOT NULL AND created_by_mentor_id IS NULL) OR '
            '(created_by_user_id IS NULL AND created_by_mentor_id IS NOT NULL)',
            name='check_single_creator'
        ),
    )

    def __repr__(self):
        return f'<Quiz {self.title}>'

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    uploaded_by_mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=True)
    uploaded_by_admin = db.Column(db.Boolean, default=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    # options = db.relationship('Option', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    options = db.relationship('Option', backref='question', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Question {self.text[:50]}>'

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  # e.g., Maths, Science
    score = db.Column(db.Integer, default=0)  # Raw score (e.g., number of correct answers)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress_id = db.Column(db.Integer, db.ForeignKey('progress.id'), nullable=True)  # New: Link to Progress

    # Relationships
    # user = db.relationship('User', backref='quiz_attempts')
    # quiz = db.relationship('Quiz', backref='attempts', lazy='dynamic')
    # course = db.relationship('Course', backref='course_attempts', lazy='dynamic')  # Changed backref
    # progress = db.relationship('Progress', backref='quiz_attempt', uselist=False)
    # answers = db.relationship('Answer', backref='attempt', lazy='dynamic', cascade='all, delete-orphan')
    # Relationships
    user = db.relationship('User', backref='quiz_attempts')
    # quiz = db.relationship('Quiz', backref='quiz_attempts')
    quiz = db.relationship('Quiz', back_populates='attempts')
    course = db.relationship('Course', back_populates='quiz_attempts')
    progress = db.relationship('Progress', backref='quiz_attempt', uselist=False)
    answers = db.relationship('Answer', backref='attempt', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<QuizAttempt user_id={self.user_id} quiz_id={self.quiz_id} score={self.score}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)

    # Relationships (optional but useful for easier joins)
    # question = db.relationship('Question', backref='answers', lazy='dynamic')
    # selected_option = db.relationship('Option', backref='answers_selected', lazy=True)
    # Relationships
    question = db.relationship('Question', backref='answers')
    selected_option = db.relationship('Option', backref='selected_answers')

    def __repr__(self):
        return f'<Answer attempt_id={self.attempt_id} question_id={self.question_id}>'
    










'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Quiz</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <style>
        body { background-color: #f3e8ff; color: #4a0072; }
        .navbar { background-color: #6a1b9a; }
        .navbar-brand, .nav-link { color: white !important; }
        .navbar-nav .nav-link:hover { color: #e1bee7 !important; }
        .card { border-radius: 1rem; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); background-color: #fff; }
        h1 { color: #6a1b9a; }
        .btn-primary { background-color: #6a1b9a; border: none; }
        .btn-primary:hover { background-color: #8e24aa; }
        .btn-secondary { background-color: #ab47bc; border: none; }
        .btn-secondary:hover { background-color: #ba68c8; }
        .btn-danger { background-color: #c2185b; border: none; }
        .btn-danger:hover { background-color: #e91e63; }
        .is-invalid { border-color: #dc3545; }
        .invalid-feedback { display: block; color: #dc3545; }
    </style>

</head>
<body>
    <!-- Navbar -->
<nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
      <a class="navbar-brand" href="{{ url_for('LandingPage') }}">EduBridge</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
        data-bs-target="#navbarNav" aria-controls="navbarNav"
        aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><a class="nav-link" href="{{ url_for('all_course') }}">Courses</a></li>
          <li class="nav-item"><a class="nav-link" href="{{ url_for('quiz_list') }}">Quiz</a></li>
        </ul>
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search">
          <button class="btn btn-outline-light" type="submit">Search</button>
        </form>
      </div>
    </div>
  </nav>

  <!-- Main Content -->
    <div class="container my-5">
        <div class="card p-4">
          <h1 class="text-center mb-4">Edit Quiz</h1>
      
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form id="quizForm" action="{{ url_for('edit_quiz', quiz_id=quiz.id) }}" method="POST">
            <div class="mb-3">
                <label for="title" class="form-label">Quiz Title</label>
                <input type="text" class="form-control" id="title" name="title" value="{{ quiz.title }}" required>
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" id="description" name="description" required>{{ quiz.description }}</textarea>
            </div>
            <div class="mb-3">
                <label for="time_limit" class="form-label">Time Limit (minutes)</label>
                <input type="number" class="form-control" id="time_limit" name="time_limit" value="{{ quiz.time_limit }}" required>
            </div>
            <div class="mb-3">
                <label for="language" class="form-label">Language</label>
                <select class="form-control" id="language" name="language">
                    <option value="en" {% if quiz.language == 'en' %}selected{% endif %}>English</option>
                    <option value="hi" {% if quiz.language == 'hi' %}selected{% endif %}>Hindi</option>
                    <option value="ta" {% if quiz.language == 'ta' %}selected{% endif %}>Tamil</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="course_id" class="form-label">Course</label>
                <select class="form-control" id="course_id" name="course_id" required>
                    {% for course in courses %}
                        <option value="{{ course.id }}" {% if course.id == quiz.course_id %}selected{% endif %}>{{ course.name }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <h3>Questions</h3>
            <div id="questions-container">
                {% for question in quiz.questions %}
                    {% set q_index = loop.index0 %}
                    <div class="question-block mb-4 border p-3">
                        <div class="mb-3">
                            <label class="form-label">Question {{ loop.index }}</label>
                            <input type="text" class="form-control question-text" name="question_text[]" value="{{ question.text }}" required>
                        </div>
                        <div class="options-container">
                            {% for option in question.options %}
                                <div class="mb-2 d-flex align-items-center">
                                    <input type="text" class="form-control option-text" name="options[{{ q_index }}][]" value="{{ option.text }}" required>
                                    <input type="radio" name="correct_option[{{ q_index }}]" value="{{ loop.index0 }}" {% if option.is_correct %}checked{% endif %} required>
                                    <label class="ms-2">Correct</label>
                                    <button type="button" class="btn btn-danger btn-sm ms-2 remove-option">Remove Option</button>
                                </div>
                            {% endfor %}
                            <!-- Hidden field to track correct option for this question -->
                            <input type="hidden" name="correct_option[]" value="{% for option in question.options %}{% if option.is_correct %}{{ loop.index0 }}{% endif %}{% endfor %}">
                        </div>
                        <button type="button" class="btn btn-secondary mt-2 add-option">Add Option</button>
                        <button type="button" class="btn btn-danger mt-2 remove-question">Remove Question</button>
                    </div>
                {% endfor %}
            </div>
            <button type="button" class="btn btn-primary mb-3" id="add-question">Add Question</button>
            <button type="submit" class="btn btn-success">Update Quiz</button>
        </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionBtn = document.getElementById('add-question');

    // Add new question
    addQuestionBtn.addEventListener('click', () => {
        const index = questionsContainer.children.length;
        const questionBlock = document.createElement('div');
        questionBlock.className = 'question-block mb-4 border p-3';
        questionBlock.innerHTML = `
            <div class="mb-3">
                <label class="form-label">Question ${index + 1}</label>
                <input type="text" class="form-control question-text" name="question_text[]" required>
            </div>
            <div class="options-container">
                <div class="mb-2 d-flex align-items-center">
                    <input type="text" class="form-control option-text" name="options[${index}][]" required>
                    <input type="radio" name="correct_option[${index}]" value="0" checked required>
                    <label class="ms-2">Correct</label>
                    <button type="button" class="btn btn-danger btn-sm ms-2 remove-option">Remove Option</button>
                </div>
                <div class="mb-2 d-flex align-items-center">
                    <input type="text" class="form-control option-text" name="options[${index}][]" required>
                    <input type="radio" name="correct_option[${index}]" value="1" required>
                    <label class="ms-2">Correct</label>
                    <button type="button" class="btn btn-danger btn-sm ms-2 remove-option">Remove Option</button>
                </div>
                <input type="hidden" name="correct_option[]" value="0">
            </div>
            <button type="button" class="btn btn-secondary mt-2 add-option">Add Option</button>
            <button type="button" class="btn btn-danger mt-2 remove-question">Remove Question</button>
        `;
        questionsContainer.appendChild(questionBlock);
        updateQuestionLabels();
        updateHiddenCorrectOption(questionBlock);
    });

    // Add new option
    questionsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-option')) {
            const optionsContainer = e.target.previousElementSibling;
            const questionIndex = Array.from(questionsContainer.children).indexOf(e.target.closest('.question-block'));
            const optionIndex = optionsContainer.querySelectorAll('.d-flex').length;
            const optionDiv = document.createElement('div');
            optionDiv.className = 'mb-2 d-flex align-items-center';
            optionDiv.innerHTML = `
                <input type="text" class="form-control option-text" name="options[${questionIndex}][]" required>
                <input type="radio" name="correct_option[${questionIndex}]" value="${optionIndex}" required>
                <label class="ms-2">Correct</label>
                <button type="button" class="btn btn-danger btn-sm ms-2 remove-option">Remove Option</button>
            `;
            optionsContainer.insertBefore(optionDiv, optionsContainer.querySelector('input[type="hidden"]'));
            updateHiddenCorrectOption(e.target.closest('.question-block'));
        }
    });

    // Remove option
    questionsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-option')) {
            const optionDiv = e.target.parentElement;
            const optionsContainer = optionDiv.parentElement;
            if (optionsContainer.querySelectorAll('.d-flex').length > 2) {
                optionDiv.remove();
                const questionBlock = optionsContainer.closest('.question-block');
                updateHiddenCorrectOption(questionBlock);
                // Ensure at least one correct option is selected
                const radios = optionsContainer.querySelectorAll('input[type="radio"]');
                if (!optionsContainer.querySelector('input[type="radio"]:checked')) {
                    radios[0].checked = true;
                    updateHiddenCorrectOption(questionBlock);
                }
            } else {
                alert('Each question must have at least 2 options.');
            }
        }
    });

    // Remove question
    questionsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-question')) {
            const questionBlock = e.target.closest('.question-block');
            if (questionsContainer.children.length > 1) {
                questionBlock.remove();
                updateQuestionLabels();
            } else {
                alert('Quiz must have at least one question.');
            }
        }
    });

    // Update question labels
    function updateQuestionLabels() {
        const questionBlocks = questionsContainer.querySelectorAll('.question-block');
        questionBlocks.forEach((block, index) => {
            const label = block.querySelector('.form-label');
            label.textContent = `Question ${index + 1}`;
        });
    }

    // Update hidden correct_option field based on selected radio
    function updateHiddenCorrectOption(questionBlock) {
        const optionsContainer = questionBlock.querySelector('.options-container');
        const hiddenInput = optionsContainer.querySelector('input[type="hidden"][name="correct_option[]"]');
        const selectedRadio = optionsContainer.querySelector('input[type="radio"]:checked');
        hiddenInput.value = selectedRadio ? selectedRadio.value : '0'; // Default to 0 if none selected
    }

    // Update hidden field when radio buttons change
    questionsContainer.addEventListener('change', (e) => {
        if (e.target.type === 'radio' && e.target.name.startsWith('correct_option[')) {
            const questionBlock = e.target.closest('.question-block');
            updateHiddenCorrectOption(questionBlock);
        }
    });

    // Client-side form validation
    document.getElementById('quizForm').addEventListener('submit', (e) => {
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const timeLimit = document.getElementById('time_limit').value;
        const questions = document.querySelectorAll('.question-text');
        let valid = true;

        if (!title.trim()) {
            alert('Quiz title is required.');
            valid = false;
        }
        if (!description.trim()) {
            alert('Quiz description is required.');
            valid = false;
        }
        if (!timeLimit || isNaN(timeLimit) || timeLimit <= 0) {
            alert('Valid time limit is required.');
            valid = false;
        }

        questions.forEach((q, i) => {
            if (!q.value.trim()) {
                alert(`Question ${i + 1} text is required.`);
                valid = false;
            }
            const questionOptions = document.querySelectorAll(`input[name="options[${i}][]"]`);
            if (questionOptions.length < 2) {
                alert(`Question ${i + 1} must have at least 2 options.`);
                valid = false;
            }
            questionOptions.forEach((opt, j) => {
                if (!opt.value.trim()) {
                    alert(`Option ${j + 1} for Question ${i + 1} is required.`);
                    valid = false;
                }
            });
            if (!document.querySelector(`input[name="correct_option[${i}]"]:checked`)) {
                alert(`Correct option for Question ${i + 1} is required.`);
                valid = false;
            }
        });

        if (!valid) {
            e.preventDefault();
        }
    });
});
    </script>
</html>
'''