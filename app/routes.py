from app import app, db
from base64 import b64encode
from app.models import Post, Product
from flask import redirect, request, render_template, url_for, flash
from werkzeug.utils import secure_filename

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


@app.route('/')
def index():
    return render_template('client/index.html', title='Home Page')



@app.route('/blog')
def blog():
    return render_template('client/blog.html', title='Blog')


@app.route('/post-detial-view')
def post_view():
    return render_template('client/post_view.html', title='Blog Post')


@app.route('/shop-products')
def shop():
    return render_template('client/shop.html', title='Shop')


@app.route('/contact')
def contact():
    return render_template('client/contact.html', title='Contact')


@app.route('/about')
def about():
    return render_template('client/about.html', title='About')




# Dashboard code start from here

@app.route('/dashboard')
def dashboard():
    post_count = Post.query.all()
    posts = Post.query.order_by(Post.timestamp.desc()).all()[0:5]

    query = request.args.get('query')
    if query:
        search_post = Post.query.filter(Post.title.contains(query)).all()
        return render_template('owner/owner_search_post.html', title='Search Result', search_post=search_post, query=query)

    return render_template('owner/owner_index.html', title='Admin Dashboard', posts=posts, post_count=post_count)


@app.route('/delete_post/<id>')
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('post'))


@app.route('/edit_post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        post.title = request.form['title']
        img = request.files['image']
        post.image = img.read()
        post.image_name = img.filename
        post.article = request.form['article']
        db.session.commit()
        return redirect(url_for('post'))
    return render_template('owner/owner_addpost.html', title='Edit Post', post=post)



@app.route('/post')
def post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    ) 
    next_url = url_for('post', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('post', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('owner/owner_post.html', title='Post', posts=posts.items, next_url=next_url, prev_url=prev_url)



@app.route('/product')
def product():
    page = request.args.get('page', type=int)
    products = Product.query.order_by(Product.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('product', page=products.next_num) \
        if products.has_next else None
    prev_url = url_for('product', page=products.prev_num) \
        if products.has_prev else None

    return render_template('owner/owner_product.html', title='Product', products=products.items, next_url=next_url, prev_url=prev_url)



@app.route('/subscriber')
def subscriber():
    return render_template('owner/owner_subscriber.html', title='Subscriber')




def allowed_image(filename):

    if not '.' in filename:
        flash("File must have '.' !")
        return False

    ext = filename.rsplit('.',1)[1]
    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        flash('File must be PNG, JPG, JPEG, GIF !')
        return False



@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
    posts = Post.query.all()
    if request.method == 'POST':
        title = request.form['title']
        article = request.form['article']


        for check_title in posts:
            if title == check_title.title:
                flash('Title already present chose a different title!')
                return redirect(url_for('addpost'))


        image = request.files['image']

        if image.filename == '':
            flash('File must have name!')
            return redirect(url_for('addpost'))

        if allowed_image(image.filename):
            image_name = secure_filename(image.filename)

            new_post = Post(title=title, image=image.read(), image_name=image_name, article=article)
            db.session.add(new_post)
            db.session.commit()
            flash('Post successfully added!')
            return redirect(url_for('addpost'))
    return render_template('owner/owner_addpost.html', title='Add Post', post=None)



@app.route('/owner_post_view/<id>')
def owner_post_view(id):
    post = Post.query.filter_by(id=id).first()
    image = b64encode(post.image).decode("utf-8")
    post.article_views = post.article_views + 1
    db.session.commit()
    return render_template('owner/owner_post_view.html', title='Post Detial View', post=post, image=image)



@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        product_url = request.form['product_url']
        product_image = request.files['product_image']
        
        if product_image.filename == '':
            flash('File must have name!')
            return redirect(url_for('addproduct'))

        if allowed_image(product_image.filename):
            product_image_name = secure_filename(product_image.filename)

            new_product = Product(title=title, 
                                 description=description, 
                                 product_url=product_url, 
                                 product_image=product_image.read(), 
                                 product_image_name=product_image_name)
            db.session.add(new_product)
            db.session.commit()
            flash('Product successfully added!')
            return redirect(url_for('addproduct'))

    return render_template('owner/owner_addproduct.html', title='Add Product')



@app.route('/owner_product_view/<id>')
def owner_product_view(id):
    product = Product.query.filter_by(id=id).first()
    image = b64encode(product.product_image).decode('utf-8')
    return render_template('owner/owner_product_view.html', title='Product Detial View', product=product, image=image)


# End Dashboard