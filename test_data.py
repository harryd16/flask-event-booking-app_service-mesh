import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random
import hashlib
from werkzeug import generate_password_hash, check_password_hash

from models import * # User, Event, Ticket
basedir = os.path.abspath(os.path.dirname(__file__))


NUM_OF_TEST_EVENTS = 100
NUM_OF_TEST_USERS = 19
NUM_OF_TEST_USERS_EVENT_MANAGER = 3
NUM_OF_TEST_USERS_ADMINISTRATOR = 3

DISCOUNT_CODES = {'5OFF':5, '10OFF': 10, '30OFF':30, 'FREE':100}

EVENT_TITLES = ['A Flair to Remember', 'A Series of Fortunate Events', 'Affairs to Remember',
        'All-Season Events', 'All Ways Events', 'Alter-ations',
        'Argyle', 'Belle of the Ball', 'Be Our Guest',
        'Big Day', 'Black Cloth', 'Black Tie Productions',
        'Bowtie', 'Celebrations', 'Ceremony Events',
        'Checklist Event Planning', '(City Name) Event Planners', 'Corporate Affairs',
        'Corroboree', 'Down the Aisle', 'Dream Wedding',
        'Effortless Events', 'Elevated', 'Enchanted Events',
        'Envisioned Events', 'Epic Events', 'EventAbility',
        'Event Guard', 'Event Horizon', 'Event Network',
        'Eventive', 'Eventor', 'Events Mean Business',
        'Events on (Street Name)', 'ExcelEvent', 'Exquisite Events',
        'Extraordinary Events', 'Fab Functions', 'Flawless Functions',
        'Formal Functions', 'Fun Done', 'Gathered',
        'Gorgeous Galas', 'Happily Ever After', 'Happenings',
        'iDo Events', 'Inspired Events', '(Last Name) and Associates',
        'Magnificent Moments', 'Man With a Plan', 'Moments in Time',
        'Monumental Event Planning', 'Occasions', 'On Point Planning',
        'On the Agenda', 'Ovation', 'Outstanding Occasions',
        'Party Productions', 'Panache', 'Perfect Plan',
        'Phenomenal Event Planning', 'Picture Perfect', 'Plan and Simple',
        'PlanIt Earth', 'Plan on It', 'Plan on Perfection',
        'Plantastic', 'Posh Events', 'Precious Memories',
        'Precision Planning', 'Pride Event Planning', 'Pro Incidents',
        'Rare Affairs', 'Receptions by (Name)', 'Rel-Event',
        'Revelry', 'Salut', 'Serendipity',
        'Smooth Operations', 'Social Hour Productions', 'Something to Remember',
        'Splendid Soirees', 'Storytellers Event Planning', 'The Event Collective',
        'The Event Concierge', 'The Event Corp.', 'The Function Junction',
        'Three Cheers', 'Turnkey Events', 'Unforgettable Events',
        'VenYou', 'Weddings Unveiled', 'White Tent Events',
        'Without a Hitch', 'Wonder Works Event Planning', 'WOW Event Planning',
        'You\'re Invited', '(Your Name) Events', '(Your Last Name) & (Business Partner Last Name)',
        '(Year) Productions', '1000 Words Event Photography']

EVENT_DESCRIPTION = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mauris pharetra et ultrices neque ornare aenean euismod elementum nisi. At in tellus integer feugiat scelerisque varius morbi enim nunc. Risus in hendrerit gravida rutrum quisque non tellus orci ac. Velit aliquet sagittis id consectetur purus. Curabitur gravida arcu ac tortor dignissim convallis aenean et tortor. Et netus et malesuada fames ac turpis egestas. Id faucibus nisl tincidunt eget. Malesuada bibendum arcu vitae elementum curabitur vitae nunc. In pellentesque massa placerat duis ultricies lacus sed. Tristique senectus et netus et malesuada fames ac. Quis vel eros donec ac odio tempor orci. Purus sit amet volutpat consequat mauris. A scelerisque purus semper eget. Fermentum leo vel orci porta non. Fermentum dui faucibus in ornare quam viverra. Sed risus pretium quam vulputate dignissim suspendisse in est. Velit euismod in pellentesque massa placerat duis ultricies lacus sed. Quis blandit turpis cursus in hac habitasse platea dictumst quisque. Ipsum suspendisse ultrices gravida dictum.

    Enim diam vulputate ut pharetra sit. Amet tellus cras adipiscing enim. Imperdiet sed euismod nisi porta lorem mollis aliquam. Habitasse platea dictumst vestibulum rhoncus est pellentesque. Felis bibendum ut tristique et egestas quis. Vitae et leo duis ut diam quam nulla porttitor massa. Sollicitudin nibh sit amet commodo. Sit amet mauris commodo quis imperdiet massa tincidunt nunc. Sed euismod nisi porta lorem mollis aliquam ut. Id diam maecenas ultricies mi eget mauris pharetra et ultrices. Commodo quis imperdiet massa tincidunt nunc pulvinar sapien et.

    Dignissim sodales ut eu sem integer vitae justo. Feugiat nibh sed pulvinar proin gravida hendrerit. Integer enim neque volutpat ac tincidunt vitae semper. Lectus urna duis convallis convallis tellus. Et egestas quis ipsum suspendisse ultrices gravida. Quis auctor elit sed vulputate mi sit amet mauris. Eget arcu dictum varius duis at consectetur lorem donec massa. Et egestas quis ipsum suspendisse. Eu consequat ac felis donec. Arcu felis bibendum ut tristique et. Sed sed risus pretium quam vulputate. Posuere sollicitudin aliquam ultrices sagittis orci a. Turpis massa sed elementum tempus egestas. Est placerat in egestas erat imperdiet. Eu sem integer vitae justo eget magna fermentum iaculis. Nunc aliquet bibendum enim facilisis. Natoque penatibus et magnis dis parturient montes nascetur ridiculus.

    Dui ut ornare lectus sit amet. Felis donec et odio pellentesque diam volutpat. Quis blandit turpis cursus in hac habitasse. Amet aliquam id diam maecenas ultricies mi eget mauris pharetra. Aliquam ut porttitor leo a diam sollicitudin tempor id eu. Luctus accumsan tortor posuere ac ut consequat semper viverra nam. Scelerisque purus semper eget duis at tellus at urna. Massa sapien faucibus et molestie ac feugiat sed. Ut eu sem integer vitae justo eget magna fermentum iaculis. Quam adipiscing vitae proin sagittis.

    Ultricies lacus sed turpis tincidunt id aliquet risus. Mattis nunc sed blandit libero volutpat sed cras ornare. In tellus integer feugiat scelerisque varius morbi enim nunc. Vel fringilla est ullamcorper eget nulla facilisi etiam dignissim diam. Imperdiet massa tincidunt nunc pulvinar sapien et. Pharetra vel turpis nunc eget lorem dolor. Sapien faucibus et molestie ac feugiat sed lectus vestibulum. Diam in arcu cursus euismod quis viverra nibh cras pulvinar. Ultricies mi quis hendrerit dolor
    magna eget est. Ipsum consequat nisl vel pretium lectus quam id leo. Semper viverra nam libero justo laoreet sit amet cursus sit. Porttitor eget dolor morbi non arcu.'''

USER_TEST_USERNAMES = [
    'test_user_al4342',
    'test_user_jf5932',
    'test_user_sf424',
    'test_user_os3522',
    'test_user_ho4856',
    'test_user_gf0945',
    'test_user_hg4582',
    'test_user_gj3583',
    'test_user_ab4253',
    'test_user_ab3945',
    'test_user_ac3852',
    'test_user_sjf3466',
    'test_user_sjg4523',
    'test_user_sn4860',
    'test_user_sn4360',
    'test_user_sh8530',
    'test_event_user_dh48690',
    'test_event_user_sd58690',
    'test_admin_sd97843',
    'test_admin_sg06849',

]

EVENT_LOCATIONS = [
    'Duck Pond Lawn',
    'McKinnon Lawn',
    '"The Yard" Cafe',
    'Building 1 Room 3',
    'Jugglers Lawn',
    'Oval No. 2',
    'Oval No. 1',
    'Oval No. 4',
    'Hockey Field',
    'UniActive',
    'Library',
    'Koolabong',
    'Building 3',
    'Uni Hall',
    'Uni Shop',
    'Building 17'
]

PERMISSION_ENUMS = [
    Permission.BASE_LEVEL,
    Permission.EVENT_MANAGER,
    Permission.ADMINISTRATOR
]

RANDOM_EVENT_DATETIME_START = datetime.datetime.strptime('28/5/2019 12:00', '%d/%m/%Y %H:%M')
RANDOM_EVENT_DATETIME_END   = datetime.datetime.strptime('28/12/2019 12:00', '%d/%m/%Y %H:%M')

def random_datetime():
    delta = RANDOM_EVENT_DATETIME_END - RANDOM_EVENT_DATETIME_START
    delta_in_seconds = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(delta_in_seconds)

    return RANDOM_EVENT_DATETIME_START + timedelta(seconds=random_second)


    #return datetime.datetime( 2019, random.randint(1,12), random.randint(1,28), random.randint(0,23), random.randint(0,59), random.randint(0,59), random.randint(0,1000000), None)

def main():
    engine = create_engine('sqlite:////' + os.path.join(basedir, 'data.sqlite'))
    Session = sessionmaker(bind=engine)
    session = Session()

    random.seed()


    # Users
    for i in range(0, NUM_OF_TEST_USERS):
        id = i
        username = USER_TEST_USERNAMES[i]
        password = 'testpass'

        if i > ( NUM_OF_TEST_USERS - (NUM_OF_TEST_USERS_EVENT_MANAGER + NUM_OF_TEST_USERS_ADMINISTRATOR) ):
            if i > (NUM_OF_TEST_USERS - NUM_OF_TEST_USERS_ADMINISTRATOR):
                permission = Permission.ADMINISTRATOR
            else:
                permission = Permission.EVENT_MANAGER
        else:
            permission = Permission.BASE_LEVEL

        new_user = User( username, password, permission )

        session.add(new_user)


    # Events
    for i in range(0, NUM_OF_TEST_EVENTS):
        id = i
        title = EVENT_TITLES[i]
        response_going = 0
        response_interested = random.randint(0,50)
        event_datetime = random_datetime()
        location = EVENT_LOCATIONS[random.randint(0,15)]
        description = EVENT_DESCRIPTION[random.randint(0,1500):random.randint(1500,3700)]
        capacity = random.randint(50,100)
        user = session.query(User).get(random.randint(NUM_OF_TEST_USERS - (NUM_OF_TEST_USERS_EVENT_MANAGER + NUM_OF_TEST_USERS_ADMINISTRATOR), NUM_OF_TEST_USERS))
        sessions = random.randint(0,3)

        new_event = Event(id, title, event_datetime, location, description, capacity, user, sessions)
        new_event.set_response_going(response_going)
        new_event.set_response_interested(response_interested)

        session.add(new_event)

    # Tickets
    users = session.query(User).all()
    discount_keys = DISCOUNT_CODES.keys()
    for event in session.query(Event).all():
        for i in range(0, random.randint(0, len(DISCOUNT_CODES)-1)):
            new_discount = Discount( event.get_id(), discount_keys[i], DISCOUNT_CODES[discount_keys[i]] )
            session.add(new_discount)

        for i in range(0, random.randint(0, event.capacity)):
            user_pool = list(users)
            if event.get_sessions() > 1:
                session_number = random.randint(1, event.get_sessions())
            else:
                session_number = 1
            quantity = 1
            event.response_going += 1
            ticket_user = random.randint(0, len(user_pool)-1)
            new_ticket = Ticket(
                    user=user_pool[ticket_user],
                    event=event,
                    session_number=session_number,
                    timestamp=event.date_created,
                    quantity=quantity
            )
            user_pool.pop(ticket_user)
            session.add(new_ticket)

    session.commit()

if __name__ == '__main__':
    main()
