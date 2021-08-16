import random
import string

def random_string_generator_user(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_user_id_generator(instance):
	user_new_id= random_string_generator_user()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(user_id=user_new_id).exists()
	if qs_exists:
		return unique_user_id_generator(instance)
	return user_new_id


def random_string_generator_grad_id(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_grade_id_generator(instance):
	grade_new_id= random_string_generator_grad_id()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(grade_id=grade_new_id).exists()
	if qs_exists:
		return unique_grade_id_generator(instance)
	return grade_new_id


def random_string_generator_session_id(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_session_id_generator(instance):
	session_new_id= random_string_generator_session_id()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(session_id=session_new_id).exists()
	if qs_exists:
		return unique_session_id_generator(instance)
	return session_new_id