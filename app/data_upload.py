from pydantic import BaseModel

from app.models import Character

class CharacterCreate(BaseModel):
    name: str
    source_media: str
    genre: str
    reference_picture: str
    reference_link: str

# Read CSV file
def udate_characters(db, csv_data):
    for row in csv_data:
        character_data = CharacterCreate(
            name=row['Character Name'],
            source_media=row['Source Media'],
            genre=row['Genre'],
            reference_picture=row['Image URL'],
            reference_link=row['Reference URL']
        )

        existing_character = db.query(Character).filter_by(
            name=character_data.name,
            source_media=character_data.source_media
        ).first()

        if existing_character:
            # Update existing character
            for key, value in character_data.dict().items():
                setattr(existing_character, key, value)
            existing_character.active = True
        else:
            # Create new character
            new_character = Character(**character_data.dict(), active=True)
            db.add(new_character)

    db.commit()
    return {"message": "CSV file processed successfully"}