import pandas as pd
import time

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to No. """
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, param_customer_name, param_hotel):
        self.customer_name = param_customer_name
        self.hotel = param_hotel

    def generate(self):
        booked_on = time.strftime("%b %d %Y %H:%M:%S")

        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.hotel_name}
        Booked on: {booked_on}
        """
        return content


class CreditCard:
    def __init__(self, param_number):
        self.card_number = param_number

    def validate(self, param_expiration, param_holder, param_cvc):
        card_data = {"number": self.card_number, "expiration": param_expiration,
                     "holder": param_holder, "cvc": param_cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, param_given_password):
        pwd = df_cards_security.loc[df_cards_security["number"] == self.card_number, "password"].squeeze()
        if pwd == param_given_password:
            return True
        else:
            return False


print(df)
print("\n")


while True:
    hotel_ID = input("Enter the ID of the hotel or exit: ")

    if hotel_ID.startswith("exit"):
        break
    elif len(df.loc[df["id"] == hotel_ID]) <= 0:
        print("Your provided Hotel ID does not exist in our list.")
        continue
    else:
        hotel = Hotel(hotel_ID)

        if hotel.available():
            card_number = input("Enter your credit card number: ")
            credit_card = SecureCreditCard(card_number)

            expiration = input("Enter the expiration date (mm/yy): ")
            holder = input("Enter the holder name: ")
            cvc = input("Enter the CVC: ")

            if credit_card.validate(param_expiration=expiration, param_holder=holder.upper(), param_cvc=cvc):
                given_pwd = input("Enter your credit card password: ")

                if credit_card.authenticate(param_given_password=given_pwd):
                    customer_name = input("Enter your name: ")
                    # Book hotel
                    hotel.book()
                    reservation_ticket = ReservationTicket(param_customer_name=customer_name.title(), param_hotel=hotel)
                    print(reservation_ticket.generate())
                    break

                else:
                    print("Credit card authentication failed.")
            else:
                print("There was a problem with your payment.")
        else:
            print("Your selected hotel is full now.")

print("Thank you and See you again!")






















































