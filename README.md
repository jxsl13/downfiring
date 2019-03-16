# Downfiring [![Donate with Ethereum](https://en.cryptobadges.io/badge/micro/0x66a1a316413A937FBf9b539aa47F65DCB04A361B)](https://en.cryptobadges.io/donate/0x66a1a316413A937FBf9b539aa47F65DCB04A361B) [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Q344HYP6A5DMN&source=url)

## What is Downfiring supposed to be?
An Upfiring(.ufr) file hosting solution based on Django.
It is supposed to be an open source alternative to e.g. [https://ufrhub.com](#).
This project is mainly for learning purposes.

Downfiring is supposed to become a webservice software that provides a decent user interface for uploading and sharing your .ufr files.
I want to create a service that aggregates .ufr files and spreads them to any other instance of this webservice, meaning one person hosts an instance of Downfiring and aggregates some files.
Another person starts hosting an instance of Downfiring and aggregates also some .ufr files. 
For someone looking for a specific file, it would take a lot of time searching the web on every Downfiring instance to find his/her needed file.
Thus Downfiring will, hopefully, provide a REST-API in order to poll other registered Downfiring instances for their whole database and hopefully the other way around.

#### The question remains, how is he "federated" database polling  going to be handled:
##### First thought:
- I(Downfiring hoster) found another Downfiring instance and try to access its data, so I send a request to that instance.
- The instance sends a response and asks for my access keys first(should be fully automatically between instances)
- After the remote instance updated its database with my accumulated data, I receive an access key from that instance in order to update my database.


