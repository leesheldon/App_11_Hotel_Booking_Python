import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")


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
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.hotel_name}
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


print(df)
print("\n")
hotel_ID = input("Enter the ID of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    customer_name = input("Enter your name: ")

    credit_card = CreditCard()
    if credit_card.validate():
        # Book hotel
        hotel.book()
        reservation_ticket = ReservationTicket(param_customer_name=customer_name, param_hotel=hotel)
        print(reservation_ticket.generate())
    else:
        print("There was a problem with your payment.")
else:
    print("Your selected hotel is full now.")





















































