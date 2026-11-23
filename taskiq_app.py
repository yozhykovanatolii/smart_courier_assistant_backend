from taskiq import SmartRetryMiddleware
from taskiq_redis import RedisStreamBroker
from clients.mail_client import send_verification_letter
from config import settings


broker = RedisStreamBroker(
    url=settings.broker_redis_url,
).with_middlewares(SmartRetryMiddleware(
    default_retry_count=4,
    default_delay=10,
    use_jitter=True,
    use_delay_exponent=True,
    max_delay_exponent=120,
))

@broker.task(retry_on_error=True)
async def send_email_letter(recipient_email: str, otp_code: str):
    await send_verification_letter(recipient_email, otp_code)