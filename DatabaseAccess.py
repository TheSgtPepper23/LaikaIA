from Models import User, Score
from datetime import date
from playhouse.shortcuts import model_to_dict
import peewee as pw

class DbMethods:

    def user_log_in(self, username, password):
        """
        Let log in a user in the game
        return:
        2 if the user is admin
        1 if everything is OK
        0 if the password don't match
        -1 if the user doesn't exists
        """
        response = None
        try:
            user = User.get(User.username == username)
            if user.is_admin == 1:
                if user.password == password:
                    response = 2
                else:
                    response = 0
            else:
                if user.password == password:
                    response = 1
                else:
                    response = 0
        except User.DoesNotExist:
            response = -1
        finally:
            return response

    def add_player(self, user_in, pass_in):
        """
        Add a player to the database game
        return:
        True if everything is OK
        False if the user already exists
        """
        exists = False

        for user in User.select():
            if user_in.upper() == user.username.upper() and user.is_active == 1:
                exists = True
                response = False

        if not exists:
            user = User(
                username = user_in, password = pass_in, is_admin=0, is_active=1)
            user.save()
            try:
                score = Score(score=0, date=date.today(), id_user = user.id_user)
                score.save()
                response = True
            except AttributeError:
                response = False

        return response

    def select_users(self, username):
        """Returns all the users of the database in case no value is specified,
            otherwise it returns those that match the user name."""
        users = []
        for user in User.select().where((User.username.startswith(username)) &
        (User.is_admin == 0) & (User.is_active == 1)).order_by(User.username.asc()):
            users.append(model_to_dict(user))
        return users

    def delete_user(self, username):
        """Delete a Player, if exists, from the database game"""
        try:
            user = User.get(User.username == username)
            user.is_active = 0
            user.save()
            response = True
        except User.DoesNotExist:
            user = None
            response = False
        finally:
            return response

    def change_user_information(self, user_in, pass_in):
        """Change the password of a Player in the database game"""
        try:
            change_info = User.update(password = pass_in).where(
                User.username == user_in)
            change_info.execute()
            response = True
        except AttributeError:
            response = False
        finally:
            return response

    def select_best_players(self):
        """Select all the players in the database game ordered by their score"""
        users_list = []
        users_score = Score.select().join(User).order_by(Score.score.desc())

        for score in users_score:
            if score.id_user.is_active:
                username_and_score = (score.id_user.username, score.score)
                users_list.append(username_and_score)
        return users_list
