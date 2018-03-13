#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Models import User, Score
from xmlrpc.server import SimpleXMLRPCServer
from datetime import date
from playhouse.shortcuts import model_to_dict, dict_to_model
import peewee as pw
import json
import xmlrpc.client
import threading

def change_user_to_waiting(user_ip):
    """Change the status of the standby user to waiting"""
    global users_connected
    user_ip = json.loads(user_ip)
    for _, data in users_connected.items():
        if data["ip"] == user_ip:
            data["state"] = "waiting"

def side_choosed(players):
    """Send a signal for the opponent to advance to the next window"""
    global users_connected
    players = json.loads(players)
    opponent_ip = users_connected[players["username"]]["opponent"]

    for _,data in users_connected.items():
        if data["ip"] == opponent_ip:
            opponent_port = data["port"]

    opponent_client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(opponent_ip, opponent_port))
    opponent_client.side_choosed(json.dumps(players["opponent_side"]))

def retrieve_waiting_users():
    """Retrieve users who are in the waiting state"""
    global users_connected
    users_waiting = []

    for user, data in users_connected.items():
        if data["state"] == "waiting":
            users_waiting.append(user)

    return json.dumps(users_waiting)

def set_points_to_winner(username):
    """Award points to the winner of the game"""
    win_player = User.get(User.username == username)
    scores = Score.select().where(Score.id_user == win_player.id_user).order_by(Score.score.asc())
    best_score = scores[0]
    puntuation = best_score.score + 100
    score = Score(score = puntuation, date = date.today(), id_user = win_player.id_user)
    score.save()

def set_opponent(players):
    """Assign the opponent's IP in the dictionary of connected users"""
    global users_connected
    players = json.loads(players)
    host_username = players["username"]
    guest_username = players["opponent"]
    for key, data in users_connected.items():
        if key == host_username:
            data["opponent"] = users_connected[guest_username]["ip"]
            data["state"] = "playing"
        if key == guest_username:
            data["opponent"] = users_connected[host_username]["ip"]
            data["state"] = "playing"

    ip_host = users_connected[host_username]["ip"]
    port_host = users_connected[host_username]["port"]

    host_client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip_host, port_host))
    host_client.go_to_select_side()

def hurry_player(username):
    """Activate a countdown in the opponent's window"""
    global users_connected
    username = json.loads(username)
    good_player = username
    lazy_player_ip = users_connected[username]["opponent"]

    for key, data in users_connected.items():
        if data["ip"] == lazy_player_ip:
            lazy_player_port = data["port"]

    lazy_client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(lazy_player_ip, lazy_player_port))
    lazy_client.countdown()

def hit_opponent(hit_info):
    """Sends the coordinate to the opponent and the attacker's username"""
    global users_connected
    hit_info = json.loads(hit_info)
    opponent_ip = users_connected[hit_info["username"]]["opponent"]

    for key, data in users_connected.items():
        if data["ip"] == opponent_ip:
            opponent = key
            opponent_port = data["port"]

    hit_send = {}
    hit_send["username"] = opponent
    hit_send["coordinate"] = hit_info["coordinate"]

    opponent_client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(opponent_ip, opponent_port))
    opponent_client.hit_coordinate(json.dumps(hit_send))


def set_winner(looser):
    """Define the winner of the game and call the function that grants the corresponding points"""
    global users_connected
    looser = json.loads(looser)
    winner_ip = users_connected[looser]["opponent"]

    for key, data in users_connected.items():
        if data["ip"] == winner_ip:
            winner = key
            winner_port = data["port"]

    set_points_to_winner(winner)
    winner_client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(winner_ip, winner_port))
    winner_client.message_winner()



if __name__ == '__main__':
    functions = [change_user_to_waiting, side_choosed, user_exists, user_log_in, add_player,
                 change_user_information, select_users, delete_user, select_best_players,
                 retrieve_waiting_users, set_opponent, hurry_player, hit_opponent, set_winner]

    server = ServerThread()

    for function in functions:
        server.add_function(function)

    server.start()

    print("Servidor corriendo en {0}:{1}".format(server.host, server.port))
