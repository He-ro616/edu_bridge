from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy
db = SQLAlchemy()

# model for stroing all the quiz created
'''
1. title of the quiz
2. quiz description
3. who create the quiz---> ['mentor' or 'admin']
4. total time to complete the quiz
5. quiz belongs to which course
6. language of the course
7. when it create
'''
# model for storing all the questions
'''
1. storing all the question related to each quiz with unique key
2. whose question is belong to which quiz--->
'''
# model for storing all the answer related to each quiz
'''
1. store all the answers related to each question.
2. whose options belong to which question.
'''

#model for storing the quiz attempt
'''
1. store inforamtion about the user's attempte like which quiz user attempted, and their frequency.
2. store information about the user's score, time taken, and completion status.
'''

# store the answer choose by the user during the quiz.
'''
1. store the answer selected by the user for each question.
2. store the question ID to which the answer belongs.
3. store the user ID for tracking the user's response.
4. store the timestamp of when the answer was selected.
5. store the quiz ID to associate the answer with the specific quiz.
6. store the selected answer for reference.

'''



# <!-- <a href="{{ url_for('quiz_result', quiz_id=quiz.id) }}" class="btn btn-primary">View Details</a> -->
#                         <!-- {% if current_user.role == 'student' %}
#                         <a href="{{ url_for('attempt_quiz', quiz_id=quiz.id) }}" class="btn btn-success">Attempt Quiz</a>
#                         {% endif %} -->


# Files can be accessed through offline.
'''
1. all videos, quizzes,notes, all courses
'''

'''
<div class="mb-3">
                <label for="date_of_birth" class="form-label">{{ form.role.label }}</label>
                {{ form.role(class="form-control") }}
                {% if form.role.errors %}
                <ul class="text-danger">
                    {% for error in form.role.errors %}
                    <li>{{ error }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
            </div>
'''