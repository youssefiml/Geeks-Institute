class Phone:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.call_history = []
        self.messages = []
    
    def call(self, other_phone):
        if not isinstance(other_phone, Phone):
            raise TypeError("other_phone must be an instance of Phone")
        call_record = f"{self.phone_number} called {other_phone.phone_number}"
        print(call_record)
        self.call_history.append(call_record)
        incoming_call = f"{other_phone.phone_number} received call from {self.phone_number}"
        other_phone.call_history.append(incoming_call)
    
    def show_call_history(self):
        print(f"Call history for {self.phone_number}:")
        if not self.call_history:
            print("  No calls in history")
        else:
            for call in self.call_history:
                print(f"  {call}")
    def send_message(self, other_phone, content):
        if not isinstance(other_phone, Phone):
            raise TypeError("other_phone must be an instance of Phone")
        message = {
            'to': other_phone.phone_number,
            'from': self.phone_number,
            'content': content
        }
        print(f"Message sent from {self.phone_number} to {other_phone.phone_number}: {content}")
        self.messages.append(message)
        incoming_message = {
            'to': other_phone.phone_number,
            'from': self.phone_number,
            'content': content
        }
        other_phone.messages.append(incoming_message)
        other_phone.messages.append(incoming_message)
    
    def show_outgoing_messages(self):
        print(f"Outgoing messages from {self.phone_number}:")
        outgoing = [msg for msg in self.messages if msg['from'] == self.phone_number]
        if not outgoing:
            print("  No outgoing messages")
        else:
            for msg in outgoing:
                print(f"  To {msg['to']}: {msg['content']}")
        print()
    
    def show_incoming_messages(self):
        print(f"Incoming messages to {self.phone_number}:")
        incoming = [msg for msg in self.messages if msg['to'] == self.phone_number]
        if not incoming:
            print("  No incoming messages")
        else:
            for msg in incoming:
                print(f"  From {msg['from']}: {msg['content']}")
        print()
    
    def show_messages_from(self, phone_number):
        print(f"Messages from {phone_number} to {self.phone_number}:")
        messages_from_number = [msg for msg in self.messages 
                               if msg['from'] == phone_number and msg['to'] == self.phone_number]
        if not messages_from_number:
            print(f"  No messages from {phone_number}")
        else:
            for msg in messages_from_number:
                print(f"  {msg['content']}")
        print()


if __name__ == "__main__":
    print("TESTING PHONE CLASS :\n")
    phone1 = Phone("555-1234")
    phone2 = Phone("555-5678")
    phone3 = Phone("555-9999")
    print("1. Testing Call Functionality:")
    print("-" * 30)
    phone1.call(phone2)
    phone2.call(phone3)
    phone3.call(phone1)
    phone1.call(phone3)
    print("\n2. Testing Call History:")
    print("-" * 30)
    phone1.show_call_history()
    phone2.show_call_history()
    phone3.show_call_history()
    print("3. Testing Message Functionality:")
    print("-" * 30)
    phone1.send_message(phone2, "Hey, how are you?")
    phone2.send_message(phone1, "I'm good, thanks!")
    phone1.send_message(phone2, "Great to hear!")
    phone3.send_message(phone1, "Are you free tonight?")
    phone1.send_message(phone3, "Yes, what's up?")
    phone3.send_message(phone1, "Want to grab dinner?")
    print("\n4. Testing Message History Methods:")
    print("-" * 30)
    phone1.show_outgoing_messages()
    phone2.show_outgoing_messages()
    phone3.show_outgoing_messages()
    phone1.show_incoming_messages()
    phone2.show_incoming_messages()
    phone3.show_incoming_messages()
    phone1.show_messages_from("555-5678")
    phone1.show_messages_from("555-9999")
    phone2.show_messages_from("555-1234")
    print("5. Testing Edge Cases:")
    print("-" * 30)
    phone4 = Phone("555-0000")
    phone4.show_call_history()
    phone4.show_outgoing_messages()
    phone4.show_incoming_messages()
    phone4.show_messages_from("555-1234")
