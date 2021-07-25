import logging

from model.declarative import RawDocument
from sqlalchemy.exc import IntegrityError


def upsert_raw(session, raw_document):
    try:
        session.add(raw_document)
        session.commit()
        logging.info('Saved %s' % raw_document.identifier)

    except IntegrityError:
        session.rollback()
        existing_record = session.query(RawDocument).filter(RawDocument.gathering_source == raw_document.gathering_source,
                                                            RawDocument.collection == raw_document.collection,
                                                            RawDocument.identifier == raw_document.identifier).one()

        if existing_record.date < raw_document.date:
            try:
                session.delete(existing_record)
                session.flush()
                session.add(raw_document)
                session.commit()
                logging.info('Updated %s' % raw_document.identifier)
            except:
                session.rollback()
