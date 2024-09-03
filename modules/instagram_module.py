import logging
import json

from instagrapi import Client  # type: ignore
from instagrapi.exceptions import LoginRequired  # type: ignore
from instagrapi.exceptions import MediaUnavailable  # type: ignore

from modules.conf import logging


class InstagramBot:
    def __init__(self, username: str | None, password: str | None) -> None:
        self.cl = Client()
        self.username = username
        self.password = password
        self.is_logged_in = False

    def login(self) -> None:
        # Try to load the session if it exists
        try:
            session = self.cl.load_settings("session.json")
        except Exception as e:
            logging.error("Couldn't load session information: %s" % e)
            session = False

        login_via_session = False
        login_via_pw = False

        # Check if session is valid
        if session:
            try:
                self.cl.set_settings(session)
                self.cl.login(self.username, self.password)

                try:
                    self.cl.get_timeline_feed()
                    login_via_session = True
                except LoginRequired:
                    logging.error(
                        "Session is invalid, need to login via username and password"
                    )
                    # Session is invalid, clear settings and login with username and password
                    self.cl.set_settings({})
                    self.cl.set_uuids(session["uuids"])  # Use previous device uuids
                    self.cl.login(self.username, self.password)
                    login_via_session = True

            except Exception as e:
                logging.error("Couldn't login user using session information: %s" % e)

        # If session is not valid, login via username and password
        if not login_via_session:
            try:
                logging.info(
                    "Attempting to login via username and password. username: %s"
                    % self.username
                )
                if self.cl.login(self.username, self.password):
                    login_via_pw = True
                    # Save the new session information
                    with open("session.json", "w") as f:
                        json.dump(self.cl.get_settings(), f)
                    logging.info("Login successful, session saved.")

            except Exception as e:
                logging.error("Couldn't login user using username and password: %s" % e)

        # Raise exception if neither method is successful
        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")

        self.is_logged_in = True

    def upload_video(self, video_path: str, caption: str) -> None:
        if not self.is_logged_in:
            raise Exception("User is not logged in")
        try:
            self.cl.clip_upload(video_path, caption=caption)
        except Exception as e:
            logging.error("Couldn't upload video: %s" % e)
