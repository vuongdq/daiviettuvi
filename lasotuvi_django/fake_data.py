import os
import random
from datetime import datetime, timedelta
from django.core.files import File
from django.utils import timezone
from faker import Faker
from PIL import Image
import requests
from io import BytesIO
import pytz
from django.utils.text import slugify

from .models import Category, Tag, News, NewsImage, Course, Lesson
from django.contrib.auth.models import User

fake = Faker('vi_VN')

def download_image(url, width=800, height=600):
    """Download and resize image from URL"""
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        img.thumbnail((width, height))
        output = BytesIO()
        img.save(output, format='JPEG')
        output.seek(0)
        return output
    except:
        return None

def create_fake_data():
    # Delete all existing data
    Category.objects.all().delete()
    Tag.objects.all().delete()
    News.objects.all().delete()
    Course.objects.all().delete()
    Lesson.objects.all().delete()

    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

    # Create categories
    categories = []
    category_names = [
        'Tử Vi Cơ Bản',
        'Tử Vi Nâng Cao',
        'Tử Vi Ứng Dụng',
        'Tử Vi Kinh Doanh',
        'Tử Vi Tình Duyên',
        'Tử Vi Sự Nghiệp',
        'Tử Vi Sức Khỏe',
        'Tử Vi Gia Đình'
    ]

    for name in category_names:
        category = Category.objects.create(
            name=name,
            slug=slugify(name),
            description=fake.text(max_nb_chars=200),
            is_active=True
        )
        categories.append(category)

    # Create tags
    tags = []
    tag_names = [
        'Tử Vi', 'Chiêm Tinh', 'Phong Thủy', 'Kinh Doanh',
        'Tình Duyên', 'Sự Nghiệp', 'Sức Khỏe', 'Gia Đình',
        'Tài Chính', 'Bất Động Sản', 'Công Danh', 'Hôn Nhân'
    ]

    for name in tag_names:
        tag = Tag.objects.create(
            name=name,
            slug=slugify(name),
            description=fake.text(max_nb_chars=100),
            is_active=True
        )
        tags.append(tag)

    # Create news
    news_count = 20
    for i in range(news_count):
        title = fake.sentence()
        news = News.objects.create(
            title=title,
            slug=slugify(title),
            content=fake.text(max_nb_chars=1000),
            category=random.choice(categories),
            author=User.objects.get(username='admin'),
            is_published=True,
            is_featured=random.choice([True, False]),
            views_count=random.randint(100, 1000),
            created_at=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=pytz.UTC)
        )
        news.tags.set(random.sample(tags, random.randint(2, 4)))

        # Add thumbnail
        img_url = f'https://picsum.photos/800/600?random={i}'
        img_content = download_image(img_url)
        if img_content:
            news.thumbnail.save(f'news_{i}.jpg', File(img_content), save=True)

        # Add news images
        for j in range(random.randint(1, 3)):
            img_url = f'https://picsum.photos/800/600?random={i}{j}'
            img_content = download_image(img_url)
            if img_content:
                NewsImage.objects.create(
                    news=news,
                    image=File(img_content),
                    caption=fake.sentence()
                )

    # Create courses
    course_count = 10
    for i in range(course_count):
        title = fake.sentence()
        course = Course.objects.create(
            title=title,
            slug=slugify(title),
            description=fake.text(max_nb_chars=500),
            category=random.choice(categories),
            price=random.randint(500000, 2000000),
            discount_price=random.randint(300000, 1500000),
            duration=f'{random.randint(1, 12)} tháng',
            level=random.choice(['beginner', 'intermediate', 'advanced']),
            instructor=User.objects.get(username='admin'),
            is_published=True,
            is_featured=random.choice([True, False]),
            enrollment_count=random.randint(50, 500),
            rating=round(random.uniform(3.5, 5.0), 1),
            created_at=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=pytz.UTC)
        )

        # Add thumbnail
        img_url = f'https://picsum.photos/800/600?random={i+100}'
        img_content = download_image(img_url)
        if img_content:
            course.thumbnail.save(f'course_{i}.jpg', File(img_content), save=True)

        # Create lessons for each course
        lesson_count = random.randint(5, 15)
        for j in range(lesson_count):
            lesson = Lesson.objects.create(
                course=course,
                title=fake.sentence(),
                order=j+1,
                content=fake.text(max_nb_chars=1000),
                video_url=f'https://www.youtube.com/watch?v={fake.uuid4()}',
                duration=f'{random.randint(15, 120)} phút',
                is_free=random.choice([True, False]),
                created_at=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=pytz.UTC)
            )

if __name__ == '__main__':
    create_fake_data() 