from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initialize the app
app = Flask(__name__)

# configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the db
db = SQLAlchemy(app)

# create event model class
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    datefrom = db.Column(db.DateTime)
    dateto = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    imageurl = db.Column(db.String(200))
    status = db.Column(db.String(20))

# create member model class
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    churchname = db.Column(db.String(200))
    gender = db.Column(db.String(20))
    contactno = db.Column(db.String(50))

# create event_member model class
class EventMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    member_id = db.Column(db.Integer)
    status = db.Column(db.String(50))

# test route
@app.route('/')
def test():
    return jsonify({'message': 'Hello!, this is a test output and it means that your app is runnin!'})

# create event 
@app.route('/event', methods=['POST'])
def create_event():
    if event_data := request.get_json():
        # get date inputs
        datefrom = event_data['datefrom']
        dateto = event_data['dateto']

        # transform the json date inputs to an object which python can understand
        datefrom_object = datetime.strptime(datefrom, '%Y-%m-%d %H:%M:%S')
        dateto_object = datetime.strptime(dateto, '%Y-%m-%d %H:%M:%S')

        # create new instance
        new_event = Event(
            name=event_data['name'],
            description=event_data['description'],
            datefrom=datefrom_object,
            dateto=dateto_object,
            location=event_data['location'],
            imageurl=event_data['imageurl'],
            status=event_data['status']
        )

        # save to db
        db.session.add(new_event)
        db.session.commit()

        # create a response that the change is successful
        return jsonify({'message': 'New event has been created!'})
    else:
        return jsonify({'error': 'No data passed!'})

# Read all event 
@app.route('/event', methods=['GET'])
def read_all_events():
    if all_events := Event.query.all():
        # create a blank list 
        all_events_output = []
        for event in all_events:
            # build individual record
            each_event = {}
            each_event['id'] = event.id
            each_event['name'] = event.name
            each_event['description'] = event.description
            each_event['datefrom'] = event.datefrom
            each_event['dateto'] = event.dateto
            each_event['location'] = event.location
            each_event['imageurl'] = event.imageurl
            each_event['status'] = event.status
            # build the output list
            all_events_output.append(each_event)

        return jsonify({'events': all_events_output})
    else:
        return jsonify({'error': 'No event found!'})

# Read one event 
@app.route('/event/<id>', methods=['GET'])
def read_one_event(id):
    if one_event := Event.query.filter_by(id=id).first():
        # build individual record
        event = {}
        event['id'] = one_event.id
        event['name'] = one_event.name
        event['description'] = one_event.description
        event['datefrom'] = one_event.datefrom.strftime('%Y-%m-%d %H:%M:%S')
        event['dateto'] = one_event.dateto.strftime('%Y-%m-%d %H:%M:%S')
        event['location'] = one_event.location
        event['imageurl'] = one_event.imageurl
        event['status'] = one_event.status

        return jsonify({'event': event})
    else:
        return jsonify({'error': 'No event found!'})

@app.route('/event/<id>', methods=['PUT'])
def update_event(id):
    # check if there is data passed
    if event_data := request.get_json():
        # check if record exist
        if update_event := Event.query.filter_by(id=id).first():
            # update instance 
            update_event.name = event_data['name']
            update_event.description = event_data['description']
            update_event.datefrom = datetime.strptime(event_data['datefrom'], '%Y-%m-%d %H:%M:%S') 
            update_event.dateto = datetime.strptime(event_data['dateto'], '%Y-%m-%d %H:%M:%S') 
            update_event.location = event_data['location']
            update_event.status = event_data['status']
            # save to db
            db.session.commit()
            # throw success message 
            return jsonify({'message': 'Event has been updated!'})
        else:
            return jsonify({'error': 'No event found!'})
    else:
        return jsonify({'error': 'No data passed!'})

# delete event
@app.route('/event/<id>', methods=['DELETE'])
def delete_one_event(id):
    # check if record exist
    if delete_event := Event.query.filter_by(id=id).first():
        # delete to db!
        db.session.delete(delete_event)
        db.session.commit()
        # throw success message 
        return jsonify({'message': 'Event has been deleted!'})
    else:
        return jsonify({'error': 'No event found!'})

# create member
@app.route('/member', methods=['POST'])
def create_member():
    if member_data := request.get_json():
        # create the new member instance
        new_member = Member(
            firstname=member_data['firstname'],
            lastname=member_data['lastname'],
            churchname=member_data['churchname'],
            gender=member_data['gender'],
            contactno=member_data['contactno']
        )
        # save to db
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member has been created!'})
    else:
        return jsonify({'error': 'No data passed!'})

# read all members
@app.route('/member', methods=['GET'])
def read_all_members():
    if all_members := Member.query.all():
        # create empty list
        all_members_output = []
        for member in all_members:
            # build individual record
            each_member = {}
            each_member['id'] = member.id
            each_member['firstname'] = member.firstname
            each_member['lastname'] = member.lastname
            each_member['churchname'] = member.churchname
            each_member['gender'] = member.gender
            each_member['contactno'] = member.contactno
            # build the output list
            all_members_output.append(each_member)
        # throw success message
        return jsonify({'members': all_members_output})
    else:
        return jsonify({'error': 'No member found!'})

# read one member
@app.route('/member/<id>', methods=['GET'])
def read_one_member(id):
    if one_member := Member.query.filter_by(id=id).first():
        # build individual record
        member = {}
        member['id'] = one_member.id
        member['firstname'] = one_member.firstname
        member['lastname'] = one_member.lastname
        member['churchname'] = one_member.churchname
        member['gender'] = one_member.gender
        member['contactno'] = one_member.contactno
        # throw success message
        return jsonify({'member': member})
    else:
        return jsonify({'error': 'No member found!'})

# update one member
@app.route('/member/<id>', methods=['PUT'])
def update_member(id):
    if member_data := request.get_json():
        if update_member := Member.query.filter_by(id=id).first():
            # update the instance
            update_member.firstname = member_data['firstname']
            update_member.lastname = member_data['lastname']
            update_member.churchname = member_data['churchname']
            update_member.gender = member_data['gender']
            update_member.contactno = member_data['contactno']
            # save to db
            db.session.commit()
            # throw success message
            return jsonify({'member': 'Member has been updated!'})
        else:
            return jsonify({'error': 'No member found!'})
    else:
        return jsonify({'error': 'No data passed!'})

# delete member
@app.route('/member/<id>', methods=['DELETE'])
def delete_member(id):
    if delete_member := Member.query.filter_by(id=id).first():
        # delete to db
        db.session.delete(delete_member)
        db.session.commit()
        # throw success message
        return jsonify({'message': 'Member has been deleted!'})
    else:
        return jsonify({'error': 'No member found!'})

@app.route('/event_member', methods=['POST'])
def create_event_member():
    # check if there is data
    if event_member_data := request.get_json():
        # check if event is existing
        if event := Event.query.filter_by(id=int(event_member_data['event_id'])).first():
            # check if member is existing
            if member := Member.query.filter_by(id=int(event_member_data['member_id'])).first():
                if event_member_exist := EventMember.query.filter(
                    EventMember.event_id==int(event_member_data['event_id']),
                    EventMember.member_id==int(event_member_data['member_id'])).first():
                    return jsonify({'error': 'Event member already exist!'})
                else:
                    # create the instance
                    new_event_member = EventMember(
                        event_id=int(event_member_data['event_id']),
                        member_id=int(event_member_data['member_id']),
                        status=event_member_data['status']
                    )
                    # commit db
                    db.session.add(new_event_member)
                    db.session.commit()
                    # throw success message
                    return jsonify({'message': 'Event member has been created!'})
            else:
                return jsonify({'error': 'Member not found!'})
        else:
            return jsonify({'error': 'Event not found!'})
    else:
        return jsonify({'error': 'No data passed!'})

# read all event_member records based on given event_id
@app.route('/event_member_by_event_id/<event_id>', methods=['GET'])
def read_all_event_members_by_event_id(event_id):
    if all_event_members := EventMember.query.filter_by(event_id=event_id).all():
        # create empty list
        all_event_members_output = []
        # loop all record
        for event_member in all_event_members:
            # build individual record
            each_event_member = {}
            each_event_member['id'] = event_member.id
            each_event_member['event_id'] = event_member.event_id
            each_event_member['member_id'] = event_member.member_id
            each_event_member['status'] = event_member.status
            # build yung otuput list
            all_event_members_output.append(each_event_member)
        # throw all the gathered records
        return jsonify({'event_members': all_event_members_output})
    else:
        return jsonify({'error' : 'No event_member found!'})

# read all event_member records based on given member_id
@app.route('/event_member_by_member_id/<member_id>', methods=['GET'])
def read_all_event_members_by_member_id(member_id):
    if all_event_members := EventMember.query.filter_by(member_id=member_id).all():
        # create empty list
        all_event_members_output = []
        # loop all record
        for event_member in all_event_members:
            # build individual record
            each_event_member = {}
            each_event_member['id'] = event_member.id
            each_event_member['event_id'] = event_member.event_id
            each_event_member['member_id'] = event_member.member_id
            each_event_member['status'] = event_member.status
            # build yung otuput list
            all_event_members_output.append(each_event_member)
        # throw all the gathered records
        return jsonify({'event_members': all_event_members_output})
    else:
        return jsonify({'error' : 'No event_member found!'})

# update event_member
@app.route('/event_member/<id>', methods=['PUT'])
def update_event_member_status(id):
    if event_member_data := request.get_json():
        if update_event_member := EventMember.query.filter_by(id=id).first():
            # update the intance
            update_event_member.status = event_member_data['status']
            # save to db
            db.session.commit()
            # throw all the gathered records
            return jsonify({'message': 'EventMember status has been updated!'})
        else:
            return jsonify({'error' : 'No event_member found!'})
    else:
        return jsonify({'error' : 'No data passed!'})

# delete event_member
@app.route('/event_member/<id>', methods=['DELETE'])
def delete_event_member(id):
    if delete_event_member := EventMember.query.filter_by(id=id).first():
        # save to db
        db.session.delete(delete_event_member)
        db.session.commit()
        # throw all the gathered records
        return jsonify({'message': 'EventMember has been deleted!'})
    else:
        return jsonify({'error' : 'No event_member found!'})

# run the app
if __name__ == '__main__':
    app.run(debug=True)