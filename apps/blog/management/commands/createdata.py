from random import randint, choice
from faker import Faker

from django.core.management.base import BaseCommand
from django.db.models import Model, Max

from apps.blog.models import (
    Category, 
    CategoryTranslations, 
    Tag, 
    Post,
    Comment
)
from apps.users.models import CustomUser

locales = ["ru_RU", "en_US"]

CATEGORIES = [
    {"slug": "technology", "ru": "Технологии", "kk": "Технологиялар", "en": "Technology"},
    {"slug": "business", "ru": "Бизнес", "kk": "Бизнес", "en": "Business"},
    {"slug": "sport", "ru": "Спорт", "kk": "Спорт", "en": "Sport"},
    {"slug": "health", "ru": "Здоровье", "kk": "Денсаулық", "en": "Health"},
    {"slug": "education", "ru": "Образование", "kk": "Білім", "en": "Education"},
    {"slug": "travel", "ru": "Путешествия", "kk": "Саяхат", "en": "Travel"},
    {"slug": "food", "ru": "Еда", "kk": "Тамақ", "en": "Food"},
    {"slug": "science", "ru": "Наука", "kk": "Ғылым", "en": "Science"},
    {"slug": "culture", "ru": "Культура", "kk": "Мәдениет", "en": "Culture"},
    {"slug": "entertainment", "ru": "Развлечения", "kk": "Ойын-сауық", "en": "Entertainment"},
]

TAGS = [
    "Python",
    "Django",
    "API",
    "Backend",
    "Frontend",
    "JavaScript",
    "React",
    "Docker",
    "PostgreSQL",
    "DevOps",
    "Machine Learning",
    "AI",
    "Startups",
    "Productivity",
    "Security",
    "Cloud",
    "Microservices",
    "Testing",
    "Open Source",
    "Programming",
    "Web Development",
    "Mobile",
    "UI/UX",
    "Data Science",
    "Architecture",
]

def get_random_instance(model: Model) -> Model:
    """
    Returns random instance of ORM model
    """

    max_pk = model.objects.all().aggregate(max_pk=Max("pk"))["max_pk"]
    
    while True:
        pk = randint(1, max_pk)
        
        instance = model.objects.filter(pk=pk).first()

        if instance:
             return instance


class Command(BaseCommand):



    def handle(self, *args, **kwargs):

        faker = Faker()

        for _ in range(20):
            CustomUser.objects.create_user(
                email = faker.email(),
                first_name = faker.first_name(),
                last_name = faker.last_name(),
                password = faker.password(),
            )

        for tag in TAGS:
                Tag.objects.get_or_create(name=tag)

        for items in CATEGORIES:

            orig_category = Category.objects.get_or_create(name=items["en"], slug=items["slug"])

            for lang in ["ru", "kk", "en"]:
                CategoryTranslations.objects.get_or_create(orig_category=orig_category[0], language=lang, name=items[lang])
            
        for _ in range(30):
            post = Post.objects.create(
                author=get_random_instance(CustomUser),
                title = faker.sentence(),
                body = faker.text(100),
                category = get_random_instance(Category),
                status = choice(list(Post.TEXT_CHOICES.keys()))
            )
            
            for _ in range(randint(0,5)):
                post.tags.add(get_random_instance(Tag))
            
            post.save()

        for _ in range(100):
            Comment.objects.create(
                post = get_random_instance(Post),
                author = get_random_instance(CustomUser),
                body = faker.text(100)
            )
