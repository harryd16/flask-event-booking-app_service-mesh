from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import datetime
import random
import country_list

from models import User, Event, Ticket

100_EVENT_TITLES = ['A Flair to Remember', 'A Series of Fortunate Events', 'Affairs to Remember',
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
        'You’re Invited', '(Your Name) Events', '(Your Last Name) & (Business Partner Last Name)',
        '(Year) Productions', '1000 Words Event Photography']

EVENT_DESCRIPTION = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mauris pharetra et ultrices neque ornare aenean euismod elementum nisi. At in tellus integer feugiat scelerisque varius morbi enim nunc. Risus in hendrerit gravida rutrum quisque non tellus orci ac. Velit aliquet sagittis id consectetur purus. Curabitur gravida arcu ac tortor dignissim convallis aenean et tortor. Et netus et malesuada fames ac turpis egestas. Id faucibus nisl tincidunt eget. Malesuada bibendum arcu vitae elementum curabitur vitae nunc. In pellentesque massa placerat duis ultricies lacus sed. Tristique senectus et netus et malesuada fames ac. Quis vel eros donec ac odio tempor orci. Purus sit amet volutpat consequat mauris. A scelerisque purus semper eget. Fermentum leo vel orci porta non. Fermentum dui faucibus in ornare quam viverra. Sed risus pretium quam vulputate dignissim suspendisse in est. Velit euismod in pellentesque massa placerat duis ultricies lacus sed. Quis blandit turpis cursus in hac habitasse platea dictumst quisque. Ipsum suspendisse ultrices gravida dictum.

    Enim diam vulputate ut pharetra sit. Amet tellus cras adipiscing enim. Imperdiet sed euismod nisi porta lorem mollis aliquam. Habitasse platea dictumst vestibulum rhoncus est pellentesque. Felis bibendum ut tristique et egestas quis. Vitae et leo duis ut diam quam nulla porttitor massa. Sollicitudin nibh sit amet commodo. Sit amet mauris commodo quis imperdiet massa tincidunt nunc. Sed euismod nisi porta lorem mollis aliquam ut. Id diam maecenas ultricies mi eget mauris pharetra et ultrices. Commodo quis imperdiet massa tincidunt nunc pulvinar sapien et.

    Dignissim sodales ut eu sem integer vitae justo. Feugiat nibh sed pulvinar proin gravida hendrerit. Integer enim neque volutpat ac tincidunt vitae semper. Lectus urna duis convallis convallis tellus. Et egestas quis ipsum suspendisse ultrices gravida. Quis auctor elit sed vulputate mi sit amet mauris. Eget arcu dictum varius duis at consectetur lorem donec massa. Et egestas quis ipsum suspendisse. Eu consequat ac felis donec. Arcu felis bibendum ut tristique et. Sed sed risus pretium quam vulputate. Posuere sollicitudin aliquam ultrices sagittis orci a. Turpis massa sed elementum tempus egestas. Est placerat in egestas erat imperdiet. Eu sem integer vitae justo eget magna fermentum iaculis. Nunc aliquet bibendum enim facilisis. Natoque penatibus et magnis dis parturient montes nascetur ridiculus.

    Dui ut ornare lectus sit amet. Felis donec et odio pellentesque diam volutpat. Quis blandit turpis cursus in hac habitasse. Amet aliquam id diam maecenas ultricies mi eget mauris pharetra. Aliquam ut porttitor leo a diam sollicitudin tempor id eu. Luctus accumsan tortor posuere ac ut consequat semper viverra nam. Scelerisque purus semper eget duis at tellus at urna. Massa sapien faucibus et molestie ac feugiat sed. Ut eu sem integer vitae justo eget magna fermentum iaculis. Quam adipiscing vitae proin sagittis.

    Ultricies lacus sed turpis tincidunt id aliquet risus. Mattis nunc sed blandit libero volutpat sed cras ornare. In tellus integer feugiat scelerisque varius morbi enim nunc. Vel fringilla est ullamcorper eget nulla facilisi etiam dignissim diam. Imperdiet massa tincidunt nunc pulvinar sapien et. Pharetra vel turpis nunc eget lorem dolor. Sapien faucibus et molestie ac feugiat sed lectus vestibulum. Diam in arcu cursus euismod quis viverra nibh cras pulvinar. Ultricies mi quis hendrerit dolor
    magna eget est. Ipsum consequat nisl vel pretium lectus quam id leo. Semper viverra nam libero justo laoreet sit amet cursus sit. Porttitor eget dolor morbi non arcu.'''

def random_datetime():
    return datetime.datetime( 2019, random.randint(1,12), random.randint(1,29), random.randint(0,24), random.randint(0,60), random.randint(0,60), random.randint(0,1000000) )


if __name__ == '__main__':
    engine = create_engine('sqlite:////' + os.path.join(basedir, 'data.sqlite')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    random.seed()



    new_event = Event()
    for i in range(0,100):
        new_event.id = i
        new_event.title = 100_EVENT_TITLES[i]
        new_event.response_going = random.randint(0,50)

        session.add(new_event)
        session.commit()


