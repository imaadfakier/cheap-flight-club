# This class is responsible for sending notifications with the deal flight details.

from twilio.rest import Client
import config
import smtplib


class NotificationManager:
    """Sends an SMS and email notification containing the cheapest flight details."""

    # class attributes
    # ...

    def __init__(self):
        self.cheap_flights_data = []
        self.cheap_flight_details = []

    def send_sms_notification(self):
        client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body='Low price alert! Only £{flight_price} to fly from '.format(
                    flight_price=self.cheap_flight_details[4]
                ) + '{departure_city}-{departure_airport_iata_code} to '.format(
                    departure_city=self.cheap_flight_details[0],
                    departure_airport_iata_code=self.cheap_flight_details[2]
                ) + '{destination_city}-{destination_airport_iata_code}, from '.format(
                    destination_city=self.cheap_flight_details[1],
                    destination_airport_iata_code=self.cheap_flight_details[3]
                ) + '{outbound_date} to {inbound_date}.\n'.format(
                    outbound_date=self.cheap_flight_details[5],
                    inbound_date=self.cheap_flight_details[6],
                ) + 'Stop over city: {stop_over_city}'.format(
                    stop_over_city=self.cheap_flights_data[7]
                ),
            from_='enter phone number',
            to='enter phone number',  # change this so that it'll be whatever the user's phone number is
        )
        return message.status

    def send_email_notification(self):
        with smtplib.SMTP(host=config.SMTP_SERVER_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=config.TEST_SENDER_EMAIL, password=config.TEST_SENDER_EMAIL_PASSWORD)
            email_subject_line = 'Subject:New Low Price Flight -> {departure_city} - {destination_city}! \n\n'\
                .format(
                    departure_city=self.cheap_flight_details[0],
                    destination_city=self.cheap_flight_details[2]
                )
            email_subject_line = email_subject_line.encode()
            flight_booking_link = f'https://www.google.co.uk/flights?hl=en#flt=' \
                                  f'{self.cheap_flight_details[2]}.{self.cheap_flight_details[3]}.' \
                                  f'{self.cheap_flight_details[5]}*{self.cheap_flight_details[3]}.' \
                                  f'{self.cheap_flight_details[2]}.{self.cheap_flight_details[6]}'
            cheap_flight_info = 'Low price alert! Only \u00A3{flight_price} to fly from ' \
                                '{departure_city}-{departure_airport_iata_code} to ' \
                                '{destination_city}-{destination_airport_iata_code}, ' \
                                'from {outbound_date} to {inbound_date}\n.' \
                                'Stop over city: {stop_over_city}\n.' \
                                '{flight_booking_link}' \
                .format(
                            flight_price=self.cheap_flight_details[4],
                            departure_city=self.cheap_flight_details[0],
                            departure_airport_iata_code=self.cheap_flight_details[1],
                            destination_city=self.cheap_flight_details[2],
                            destination_airport_iata_code=self.cheap_flight_details[3],
                            outbound_date=self.cheap_flight_details[5],
                            inbound_date=self.cheap_flight_details[6],
                            stop_over_city=self.cheap_flights_data[7],
                            flight_booking_link=flight_booking_link,
                )
            cheap_flight_info = cheap_flight_info.encode('utf-8')
            connection.sendmail(
                from_addr=config.TEST_SENDER_EMAIL,
                to_addrs=config.TEST_RECEIVER_EMAIL,  # change this so that it'll be whatever the user's email is
                msg=email_subject_line + cheap_flight_info
            )
