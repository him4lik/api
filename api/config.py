from enum import Enum

class BaseEnumClass(Enum):

    @classmethod
    def get_keys(cls):
        return [x.name for x in cls]

    @classmethod
    def get_values(cls):
        return [x.value for x in cls]

    @classmethod
    def get_key_value(cls):
        return {x.name:x.value for x in cls}

class States(BaseEnumClass):
    AP = 'Andhra Pradesh'
    AR = 'Arunachal Pradesh'
    AS = 'Assam'
    BR = 'Bihar'
    CT = 'Chhattisgarh'
    GA = 'Goa'
    GJ = 'Gujarat'
    HR = 'Haryana'
    HP = 'Himachal Pradesh'
    JH = 'Jharkhand'
    KA = 'Karnataka'
    KL = 'Kerala'
    MP = 'Madhya Pradesh'
    MH = 'Maharashtra'
    MN = 'Manipur'
    ML = 'Meghalaya'
    MZ = 'Mizoram'
    NL = 'Nagaland'
    OR = 'Odisha'
    PB = 'Punjab'
    RJ = 'Rajasthan'
    SK = 'Sikkim'
    TN = 'Tamil Nadu'
    TG = 'Telangana'
    TR = 'Tripura'
    UT = 'Uttarakhand'
    UP = 'Uttar Pradesh'
    WB = 'West Bengal'
    AN = 'Andaman and Nicobar Islands'
    CH = 'Chandigarh'
    DN = 'Dadra and Nagar Haveli'
    DD = 'Daman and Diu'
    DL = 'Delhi'
    JK = 'Jammu and Kashmir'
    LA = 'Ladakh'
    LD = 'Lakshadweep'
    PY = 'Puducherry'
