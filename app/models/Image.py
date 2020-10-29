from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session
from flask import current_app as flask_app
import uuid, time

class Image():

    def __init__(self):
        return None

    def get_images(self, limit=20):
        """
        Attempts to retrieve images from database
        """
        error = None
        images = False

        try:
            database = Database()
            images = database.get_images(limit)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            raise Exception(error)
        else:
            # successfully returned Pyrebase object.
            return images

    def get_category_images(self, category, limit=20):
        
        """
        Gets the images for the category that gets passed in limits the result 
        set to 20 images
        """
        # Set inital variables
        error = None
        images = False
        
        # Tries to get the images
        try:
            database = Database()
            images = database.get_category_images(category, limit)

        # Failed to get images, raise an exception.
        except Exception as err:
            flask_app.logger.info(err)
            error = err

        # Check if we have an error.
        if error:
            #We have an error, pass it back to the controller
            raise Exception(error)
        else:
            #We have no errors, return the images
            return images

    def get_image(self, image_id):
        
        error = None
        image = False
        
        try:
            database = Database()
            image = database.get_image(image_id)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            raise Exception(error)
        else:
            return image

    def delete_image(self, image_id):
        
        error = None
        
        try:
            database = Database()
            database.delete_image(image_id)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            raise Exception(error)
        else: 
            
            return
  
    def get_user_images(self, limit=20):
        """
         Retrieves users images from the database
        """
        error = None
        images = False
        user_id = False
        if (session['user'] and session['user']['localId']):
            user_id = session['user']['localId']
        try:
            database = Database()
            images = database.get_images(limit, user_id)

        except Exception as err:
            flask_app.logger.info(err)
            error = err
       
        if error:
            raise Exception(error)
        else:
            return images

    def upload(self, request):
        """
        Request to upload image is sent to the database
        """
        image_id        = str(uuid.uuid1())
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']

        # Validates required registration fields
        error = None
        user_id = False

        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            error = 'You must be logged in to upload an image.'

        if 'image' not in request.files:
            error = 'A file is required.'
        else:
            file = request.files['image']

        if not error:
            if file.filename == '':
                error = 'A file is required.'
            elif not name:
                error = 'An name is required.'
            elif not description:
                error = 'A description is required.'
            elif not category:
                error = 'A category is required.'
            else:
                try:
                    uploader = Upload()
                    upload_location = uploader.upload(file, image_id)
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      '/' + upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           int(time.time())
                    }
                    database = Database()
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    error = err
        if error:
            flask_app.logger.info('################ UPLOAD ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            return image_id

    def update(self, image_id, request):
        flask_app.logger.info('####################### request.form #####################')
        flask_app.logger.info(request.form)
        
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']
        created_at      = request.form['created_at'] 
        upload_location = request.form['upload_location']  



        # Validates required registration fields
        error = None
        user_id = False

        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        # User tries to edit image logged out.
        else: 
            error = 'You must be logged in to update an image.'
        # User forgets to give image a name
        if not error:
            if not name:
                error = 'A name is required.'
            # User forgets to give image a discription.
            elif not description:
                error = 'A description is required.'
            # User forgets to give image a category.
            elif not category:
                error = 'A category is required.'
            else:
                """
                Creates image object for the database
                """
                try:
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           created_at
                    }
                    database = Database()
                    
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    error = err
        if error:
            flask_app.logger.info('################ UPDATE ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            return