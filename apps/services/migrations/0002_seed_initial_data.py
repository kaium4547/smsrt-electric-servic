from django.db import migrations


def seed_services(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    ServiceFeature = apps.get_model('services', 'ServiceFeature')

    data = [
        {
            'name': 'ইলেকট্রিক কাজ', 'slug': 'electric-work', 'icon': 'fas fa-bolt',
            'short': 'সম্পূর্ণ হাউজ ওয়্যারিং, মেইন লাইন, ব্রেকার সেটআপ',
            'features': [
                'সম্পূর্ণ হাউজ ওয়্যারিং',
                'ব্রেকার ও DB বোর্ড সেটআপ',
                'লোড ক্যালকুলেশন ও সার্কিট ডিজাইন',
                'মেইন লাইন ও সাব-মেইন লাইন'
            ]
        },
        {
            'name': 'সোলার প্যানেল ইনস্টলেশন', 'slug': 'solar-installation', 'icon': 'fas fa-sun',
            'short': '1KW–5KW সিস্টেম ডিজাইন ও ইনস্টলেশন',
            'features': ['প্যানেল বসানো', 'ইনভার্টার সেটআপ', 'ব্যাটারি কনফিগারেশন', 'মোবাইল মনিটরিং']
        },
        {
            'name': 'সিসিটিভি ক্যামেরা', 'slug': 'cctv-camera', 'icon': 'fas fa-video',
            'short': 'HD/IP ক্যামেরা, DVR/NVR, মোবাইল অ্যাপ',
            'features': ['ক্যামেরা ইনস্টল', 'DVR/NVR কনফিগারেশন', 'রিমোট ভিউ সেটআপ', 'রক্ষণাবেক্ষণ']
        },
        {
            'name': 'এসি ইনস্টলেশন ও সার্ভিসিং', 'slug': 'ac-service', 'icon': 'fas fa-snowflake',
            'short': 'গ্যাস রিচার্জ, ইনস্টলেশন ও মেইনটেনেন্স',
            'features': ['নতুন এসি ইনস্টল', 'গ্যাস রিফিল', 'ওয়াটার ড্রেইন সেটআপ', 'কম্প্রেসার চেক']
        },
        {
            'name': 'প্লাম্বিং ও ফিটিংস', 'slug': 'plumbing', 'icon': 'fas fa-faucet',
            'short': 'পাইপ বসানো, ড্রেনেজ, ট্যাপ/শাওয়ার ফিটিং',
            'features': ['পাইপ বসানো', 'ড্রেনেজ সিস্টেম', 'ট্যাপ/শাওয়ার ফিটিং', 'ওয়াটার হিটার সেটআপ']
        },
    ]

    for item in data:
        service, _ = Service.objects.get_or_create(
            slug=item['slug'],
            defaults={
                'name': item['name'],
                'short_description': item['short'],
                'long_description': item['short'],
                'icon_class': item['icon'],
                'available': True,
            }
        )
        for f in item['features']:
            ServiceFeature.objects.get_or_create(service=service, feature_text=f)


def unseed_services(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    for slug in ['electric-work', 'solar-installation', 'cctv-camera', 'ac-service', 'plumbing']:
        Service.objects.filter(slug=slug).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_services, unseed_services),
    ]