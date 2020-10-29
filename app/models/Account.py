from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session, flash
from flask import current_app as flask_app

class Account():

    def __init__(self):
        self.user = User()
        return None

    def register(self, request):
        """ 
        Registration method. 
    
        Processes POST request, and registers user in Firebase on success

        Parameters: 
            request (obj): The POST request object
    
        Raises: 
            error (Exception): Error from failed Firebase request
    
        """

        # Extract required fields from POST request
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Validates required registration fields
        """
         Presents error messages for registration process

        """
        error = None
        # When email field is not filled out
        if not email:
            error = 'An email is required.'
        # When password field is not filled out
        elif not password:
            error = 'Password is required.'
        # When password is under 6 characters
        elif 6 > len(password):
            error = 'Your password must be at least 6 characters long.'
        # When password confirmation field is not filled out.
        elif not password_confirm:
            error = 'Password confirmation is required.'
         # When Password and Password confirmation fields don't match
        elif password != password_confirm:
            error = 'Password and password confirmation should match.'
        else:
            try:
                user_data = {
                    "localId": "",
                    "email": email,
                    "first_name": "",
                    "last_name": "",
                    "avatar": ""
                }
                # Attempt to process valid registration request
                database = Database()
                user_auth = database.register(user_data, password)
            except Exception as err:
                # Raise error from failed Firebase request
                error = err
        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            # Return on success
            return
        
    def login(self, request):
        """
        Attempts to login using user credentials

        """
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            error = None
            # When email field is not filled in.
            if not email:
                error = 'An email is required.'
            # When password  field is not filled in.
            elif not password:
                error = 'Password is required.'
            else:
                try:
                    database = Database()
                    user = database.login(email, password)
                    # TODO Remove for production
                    #flask_app.logger.info(user)
                    self.user.set_user(user)
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        
    def update(self, request):
        """
        Updates User's First & Last Name

        """
        if request.method == 'POST':
            first_name = request.form['firstname']
            last_name = request.form['lastname']

            error = None
            # When first name field is not filled out
            if not first_name:
                error = 'A first name is required.'
            # When last name field is not filled out 
            elif not last_name:
                error = 'A last name is required.'
            else:
                """
                Checks if user has uploaded a file. If so
                it will update users avatar
                """
                if 'avatar' in request.files:
                    file = request.files['avatar']
                    if file.filename:
                        uploader = Upload()
                        avatar = uploader.upload(file, session['user']['localId'])
                        session['user']['avatar'] = "/" + avatar.strip("/")
                try:
                    session['user']['first_name'] = first_name
                    session['user']['last_name'] = last_name
                    database = Database()
                    user_auth = database.update_user(session['user'])
                    session.modified = True
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
        else:
            return
        
    def like(self, image_id, like, request):
        """
        Like method. 

        If user likes image, then that image will be added to their 
        liked images list.

        If the user unlikes image, then that iamge will be removed
        from their liked images list.
        
        """        
        changed = False
        likes = session['user']['likes']
        # User has liked Image.
        if like == 'true':
            # Check if user has already liked it
            if image_id not in likes:
                likes.append(image_id)
                changed = True
        else:
            # User unlikes image.
            if image_id in likes:
                likes.remove(image_id)
                changed = True
        # If likes are changed will be updated in the database.
        if changed:
            session['user']['likes'] = likes
            database = Database()
            database.update_user(session['user'])
            # Updates the session.
            session.modified = True

        return changed
        
    def logout(self):
        """
        Logs user out

        """
        self.user.unset_user()

