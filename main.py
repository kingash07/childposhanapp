import os
from flask import jsonify

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

app = Flask(__name__)
Bootstrap(app)
Base = declarative_base()

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///childposhandata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE STATE TABLE
class State(db.Model, Base):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(250), unique=True, nullable=False)
    # creating relationship with the District database
    districts = relationship('District', backref='state')


# CONFIGURE DISTRICT TABLE
class District(db.Model, Base):
    __tablename__ = 'district'
    id = db.Column(db.Integer, primary_key=True)
    district_name = db.Column(db.String(250), unique=True, nullable=False)
    # linking to the database district and giving column name
    states_id = db.Column('state_id', db.Integer, db.ForeignKey("state.id"), nullable=False)
    # end with linking the district and state table
    # creating relationship with the blocks database
    blocks_d_s = relationship('BlocksD', backref='district')


# CONFIGURE BLOCKS TABLE
class BlocksD(db.Model, Base):
    __tablename__ = 'blocksd'
    id = db.Column(db.Integer, primary_key=True)
    block_name = db.Column(db.String(250), unique=True, nullable=False)
    # linking to the database blocks and giving column name
    district_id = db.Column('district_id', db.Integer, db.ForeignKey("district.id"), nullable=False)
    # end with linking the blocks and district table
    sectors = relationship('Sector', backref='blocksd')


# CONFIGURE SECTOR TABLE
class Sector(db.Model, Base):
    __tablename__ = 'sector'
    id = db.Column(db.Integer, primary_key=True)
    sector_name = db.Column(db.String(250), unique=True, nullable=False)
    blocks_D_id = db.Column('block_id', db.Integer, db.ForeignKey("blocksd.id"), nullable=False)
    aws_names = relationship('AWSName', backref='sector')


# CONFIGURE AWSNAME TABLE
class AWSName(db.Model, Base):
    __tablename__ = 'awsname'
    id = db.Column(db.Integer, primary_key=True)
    aws_name = db.Column(db.String(250), nullable=False)
    sector_id = db.Column('sector_id', db.Integer, db.ForeignKey("sector.id"), nullable=False)
    villages = relationship('Village', backref='awsname')


# CONFIGURE VILLAGE TABLE
class Village(db.Model, Base):
    __tablename__ = 'village'
    id = db.Column(db.Integer, primary_key=True)
    village_town_name = db.Column(db.String(250), nullable=False)
    aws_id = db.Column('aws_id', db.Integer, db.ForeignKey('awsname.id'), nullable=False)


if not os.path.isfile('sqlite:///childposhandata.db'):
    with app.app_context():
        db.create_all()


# index page
@app.route('/')
def home():
    s_name = 'Himachal Pradesh'
    d_name = 'Kangra'
    b_name = 'Bhawarna'
    se_name = 'Bhawarna'
    a_name = 'Bhatti'
    v_name = 'Bhawarna'

    check_state_available = State.query.filter_by(state_name=s_name).first()
    check_district_available = District.query.filter_by(district_name=d_name).first()
    check_block_available = BlocksD.query.filter_by(block_name=b_name).first()
    check_sector_available = Sector.query.filter_by(sector_name=se_name).first()
    if check_state_available:
        if check_district_available:
            if check_block_available:
                if check_sector_available:
                    aws_name = AWSName(aws_name=a_name, sector_id=check_sector_available.id)
                    db.session.add(aws_name)
                    db.session.commit()
                    village = Village(village_town_name=v_name, aws_id=aws_name.id)
                    db.session.add(village)
                    db.session.commit()
                else:
                    sector = Sector(sector_name=se_name, blocks_D_id=check_block_available.id)
                    db.session.add(sector)
                    db.session.commit()
                    aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
                    db.session.add(aws_name)
                    db.session.commit()
                    village = Village(village_town_name=v_name, aws_id=aws_name.id)
                    db.session.add(village)
                    db.session.commit()
            else:
                blockc = BlocksD(block_name=b_name, district_id=check_district_available.id)
                db.session.add(blockc)
                db.session.commit()
                sector = Sector(sector_name=se_name, blocks_D_id=blockc.id)
                db.session.add(sector)
                db.session.commit()
                aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
                db.session.add(aws_name)
                db.session.commit()
                village = Village(village_town_name=v_name, aws_id=aws_name.id)
                db.session.add(village)
                db.session.commit()
        else:
            district = District(district_name=d_name, states_id=check_state_available.id)
            db.session.add(district)
            db.session.commit()
            blockc = BlocksD(block_name=b_name, district_id=district.id)
            db.session.add(blockc)
            db.session.commit()
            sector = Sector(sector_name=se_name, blocks_D_id=blockc.id)
            db.session.add(sector)
            db.session.commit()
            aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
            db.session.add(aws_name)
            db.session.commit()
            village = Village(village_town_name=v_name, aws_id=aws_name.id)
            db.session.add(village)
            db.session.commit()
    else:
        state = State(state_name=s_name)
        db.session.add(state)
        db.session.commit()
        district = District(district_name=d_name, states_id=state.id)
        db.session.add(district)
        db.session.commit()
        blockc = BlocksD(block_name=b_name, district_id=district.id)
        db.session.add(blockc)
        db.session.commit()
        sector = Sector(sector_name=se_name, blocks_D_id=blockc.id)
        db.session.add(sector)
        db.session.commit()
        aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
        db.session.add(aws_name)
        db.session.commit()
        village = Village(village_town_name=v_name, aws_id=aws_name.id)
        db.session.add(village)
        db.session.commit()
    return 'you have successfully updated'


# make API of the data using jsonify
@app.route('/api')
def all_data():
    states = db.session.query(State).all()
    data = []
    for state in states:
        state_dict = {
            'State': state.state_name,
            'Districts': []
        }
        for district in state.districts:
            district_dict = {
                'District_Name': district.district_name,
                'Blocks': [],
            }
            for block in district.blocks_d_s:
                block_dict = {
                    'Block_Name': block.block_name,
                    'Sectors': []
                }
                for sector in block.sectors:
                    sector_dict = {
                        'Sector_Name': sector.sector_name,
                        'AWSName': []
                    }
                    for aws in sector.aws_names:
                        aws_dict = {
                            'AWS_Name': aws.aws_name,
                            'Villages': []
                        }
                        for village in aws.villages:
                            vill_dict = {
                                'Village/Town_Name': village.village_town_name
                            }
                            aws_dict['Villages'].append(vill_dict)
                        sector_dict['AWSName'].append(aws_dict)
                    block_dict['Sectors'].append(sector_dict)
                district_dict['Blocks'].append(block_dict)
            state_dict['Districts'].append(district_dict)
        data.append(state_dict)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

# import pandas as pd
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import State, District, Block, Sector, AWSName
#
# # create an engine to connect to the database
# engine = create_engine('postgresql://username:password@localhost:5432/database_name')
#
# # create a session to communicate with the database
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # read the Excel file into a pandas DataFrame
# df = pd.read_excel('path/to/excel/file.xlsx')
#
# # iterate over each row of the DataFrame and insert the data into the database
# for index, row in df.iterrows():
#     # get the state name from the 'State' column
#     state_name = row['State']
#
#     # check if the state already exists in the database, and create it if it doesn't
#     state = session.query(State).filter_by(name=state_name).first()
#     if not state:
#         state = State(name=state_name)
#         session.add(state)
#
#     # get the district name from the 'District' column
#     district_name = row['District']
#
#     # check if the district already exists in the database, and create it if it doesn't
#     district = session.query(District).filter_by(name=district_name, state=state).first()
#     if not district:
#         district = District(name=district_name, state=state)
#         session.add(district)
#
#     # get the block name from the 'Block' column
#     block_name = row['Block']
#
#     # check if the block already exists in the database, and create it if it doesn't
#     block = session.query(Block).filter_by(name=block_name, district=district).first()
#     if not block:
#         block = Block(name=block_name, district=district)
#         session.add(block)
#
#     # get the sector name from the 'Sector' column
#     sector_name = row['Sector']
#
#     # check if the sector already exists in the database, and create it if it doesn't
#     sector = session.query(Sector).filter_by(name=sector_name, block=block).first()
#     if not sector:
#         sector = Sector(name=sector_name, block=block)
#         session.add(sector)
#
#     # get the AWS name from the 'AWS Name' column
#     aws_name = row['AWS Name']
#
#     # check if the AWS name already exists in the database, and create it if it doesn't
#     aws = session.query(AWSName).filter_by(name=aws_name, sector=sector).first()
#     if not aws:
#         aws = AWSName(name=aws_name, sector=sector)
#         session.add(aws)
#
# # commit the changes to the database
# session.commit()
