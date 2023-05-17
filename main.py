import os
from flask import jsonify
from collections import OrderedDict
import pandas as pd
import string
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


@app.route('/')
def homepage():
    return 'hello world'


@app.route('/csvf')
def csvs_files():
    csv_data = pd.read_csv('Master Data.csv',
                           usecols=["State Name", "District Name", "Project Name", "Sector", "AWC Name",
                                    "Village Town"])

    for index, row in csv_data.iterrows():
        # get the district name from the 'State' column
        state_name = string.capwords(row['State Name'])
        # get the district name from the 'District' column
        district_name = string.capwords(row['District Name'])
        #   get the block name from the 'Block' column
        block_name = string.capwords(row['Project Name'])
        #   get the sector name from the 'Sector' column
        sector_name = string.capwords(row['Sector'])
        #   get the AWS name from the 'AWS Name' column
        aws_name = string.capwords(row['AWC Name'])
        #   get the village name from the 'AWS Name' column
        village_name = string.capwords(str(row['Village Town']))
        #   check if the state  already exists in the database, and create it if it doesn't
        states = State.query.filter_by(state_name=state_name).first()
        #   check if the district already exists in the database, and create it if it doesn't
        district = District.query.filter_by(district_name=district_name).first()
        #   check if the block already exists in the database, and create it if it doesn't
        block = BlocksD.query.filter_by(block_name=block_name).first()
        #   check if the sector already exists in the database, and create it if it doesn't
        sector = Sector.query.filter_by(sector_name=sector_name).first()
        #   check if the AWS name already exists in the database, and create it if it doesn't
        aws = AWSName.query.filter_by(aws_name=aws_name).first()
        #   check if the village name already exists in the database, and create it if it doesn't
        village = Village.query.filter_by(village_town_name=village_name).first()
        if states:
            if district:
                if block:
                    if sector:
                        aws = AWSName(aws_name=aws_name, sector_id=sector.id)
                        db.session.add(aws)
                        db.session.commit()
                        db.session.refresh(aws)
                        village = Village(village_town_name=village_name,  aws_id=aws.id)
                        db.session.add(village)
                        db.session.commit()
                        db.session.refresh(village)
                    else:
                        sector = Sector(sector_name=sector_name, blocks_D_id=block.id)
                        db.session.add(sector)
                        db.session.commit()
                        db.session.refresh(sector)
                        aws = AWSName(aws_name=aws_name, sector_id=sector.id)
                        db.session.add(aws)
                        db.session.commit()
                        db.session.refresh(aws)
                        village = Village(village_town_name=village_name,  aws_id=aws.id)
                        db.session.add(village)
                        db.session.commit()
                        db.session.refresh(village)

                else:
                    block = BlocksD(block_name=block_name, district_id=district.id)
                    db.session.add(block)
                    db.session.commit()
                    db.session.refresh(block)
                    sector = Sector(sector_name=sector_name, blocks_D_id=block.id)
                    db.session.add(sector)
                    db.session.commit()
                    db.session.refresh(sector)
                    aws = AWSName(aws_name=aws_name, sector_id=sector.id)
                    db.session.add(aws)
                    db.session.commit()
                    db.session.refresh(aws)
                    village = Village(village_town_name=village_name,  aws_id=aws.id)
                    db.session.add(village)
                    db.session.commit()
                    db.session.refresh(village)
            else:
                district = District(district_name=district_name,  states_id=states.id)
                db.session.add(district)
                db.session.commit()
                db.session.refresh(district)
                block = BlocksD(block_name=block_name, district_id=district.id)
                db.session.add(block)
                db.session.commit()
                db.session.refresh(block)
                sector = Sector(sector_name=sector_name, blocks_D_id=block.id)
                db.session.add(sector)
                db.session.commit()
                db.session.refresh(sector)
                aws = AWSName(aws_name=aws_name,  sector_id=sector.id)
                db.session.add(aws)
                db.session.commit()
                db.session.refresh(aws)
                village = Village(village_town_name=village_name, aws_id=aws.id)
                db.session.add(village)
                db.session.commit()
                db.session.refresh(village)
        else:
            state = State(state_name=state_name,)
            db.session.add(state)
            db.session.commit()
            db.session.refresh(state)
            district = District(district_name=district_name, states_id=state.id)
            db.session.add(district)
            db.session.commit()
            db.session.refresh(district)
            block = BlocksD(block_name=block_name, district_id=district.id)
            db.session.add(block)
            db.session.commit()
            db.session.refresh(block)
            sector = Sector(sector_name=sector_name, blocks_D_id=block.id)
            db.session.add(sector)
            db.session.commit()
            db.session.refresh(sector)
            aws = AWSName(aws_name=aws_name, sector_id=sector.id)
            db.session.add(aws)
            db.session.commit()
            db.session.refresh(aws)
            village = Village(village_town_name=village_name, aws_id=aws.id)
            db.session.add(village)
            db.session.commit()
            db.session.refresh(village)
    db.session.close()
    return 'bangya re database'


# # index page
# @app.route('/add')
# def home():
#     s_name = string.capwords('himachal Pradesh')
#
#     d_name = string.capwords('Kangra')
#
#     b_name = string.capwords('Bhawarna')
#
#     se_name = string.capwords('Bhawarna')
#     a_name = string.capwords('Bhatti')
#     v_name = string.capwords('Bhawarna')
#
#     check_state_available = State.query.filter_by(state_name=s_name).first()
#     check_district_available = District.query.filter_by(district_name=d_name).first()
#     check_block_available = BlocksD.query.filter_by(block_name=b_name).first()
#     check_sector_available = Sector.query.filter_by(sector_name=se_name).first()
#     if check_state_available:
#         if check_district_available:
#             if check_block_available:
#                 if check_sector_available:
#                     aws_name = AWSName(aws_name=a_name, sector_id=check_sector_available.id)
#                     db.session.add(aws_name)
#                     db.session.commit()
#                     db.session.close()
#                     village = Village(village_town_name=v_name, aws_id=aws_name.id)
#                     db.session.add(village)
#                     db.session.commit()
#                     db.session.close()
#                 else:
#                     sector = Sector(sector_name=se_name, blocks_D_id=check_block_available.id)
#                     db.session.add(sector)
#                     db.session.commit()
#                     db.session.close()
#                     aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
#                     db.session.add(aws_name)
#                     db.session.commit()
#                     db.session.close()
#                     village = Village(village_town_name=v_name, aws_id=aws_name.id)
#                     db.session.add(village)
#                     db.session.commit()
#                     db.session.close()
#             else:
#                 blockc = BlocksD(block_name=b_name, district_id=check_district_available.id)
#                 db.session.add(blockc)
#                 db.session.commit()
#                 db.session.close()
#                 sector = Sector(sector_name=se_name, blocks_D_id=blockc.id)
#                 db.session.add(sector)
#                 db.session.commit()
#                 db.session.close()
#                 aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
#                 db.session.add(aws_name)
#                 db.session.commit()
#                 db.session.close()
#                 village = Village(village_town_name=v_name, aws_id=aws_name.id)
#                 db.session.add(village)
#                 db.session.commit()
#                 db.session.close()
#         else:
#             district = District(district_name=d_name, states_id=check_state_available.id)
#             db.session.add(district)
#             db.session.commit()
#             db.session.close()
#             blockc = BlocksD(block_name=b_name, district_id=district.id)
#             db.session.add(blockc)
#             db.session.commit()
#             db.session.close()
#             sector = Sector(sector_name=se_name, blocks_D_id=blockc.id)
#             db.session.add(sector)
#             db.session.commit()
#             db.session.close()
#             aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
#             db.session.add(aws_name)
#             db.session.commit()
#             db.session.close()
#             village = Village(village_town_name=v_name, aws_id=aws_name.id)
#             db.session.add(village)
#             db.session.commit()
#             db.session.close()
#     else:
#         state = State(state_name=s_name)
#         db.session.add(state)
#         db.session.commit()
#         db.session.close()
#         district = District(district_name=d_name, states_id=state.id)
#         db.session.add(district)
#         db.session.commit()
#         db.session.close()
#         blockc = BlocksD(block_name=b_name, district_id=district.id)
#         db.session.add(blockc)
#         db.session.commit()
#         db.session.close()
#         sector = Sector(sector_name=se_name, blocks_D_id=blockc.id)
#         db.session.add(sector)
#         db.session.commit()
#         db.session.close()
#         aws_name = AWSName(aws_name=a_name, sector_id=sector.id)
#         db.session.add(aws_name)
#         db.session.commit()
#         db.session.close()
#         village = Village(village_town_name=v_name, aws_id=aws_name.id)
#         db.session.add(village)
#         db.session.commit()
#         db.session.close()
#     return 'you have successfully updated'


# make API of the data using jsonify
@app.route('/api')
def all_data():
    states = db.session.query(State).all()
    # data = OrderedDict()
    data = []
    for state in states:
        state_dict = {
            state.state_name: [{
                'Districts': [],
            }],

        }
        for district in state.districts:
            district_dict = {
                district.district_name: [{
                    'Blocks': [],
                }],
            }
            for block in district.blocks_d_s:
                block_dict = {
                    block.block_name: [{
                        'Sectors': []
                    }],

                }
                for sector in block.sectors:
                    sector_dict = {
                        sector.sector_name: [{
                            'AWSName':
                                []
                        }]
                    }
                    for aws in sector.aws_names:
                        aws_dict = {
                            aws.aws_name: [{
                                'Villages': []
                            }]
                        }
                        for village in aws.villages:
                            vill_dict = {
                                'Village/Town_Name': village.village_town_name
                            }
                            aws_dict[aws.aws_name][0]['Villages'].append(vill_dict)
                        sector_dict[sector.sector_name][0]['AWSName'].append(aws_dict)
                    block_dict[block.block_name][0]['Sectors'].append(sector_dict)
                district_dict[district.district_name][0]['Blocks'].append(block_dict)
            state_dict[state.state_name][0]['Districts'].append(district_dict)
        data.append(state_dict)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
