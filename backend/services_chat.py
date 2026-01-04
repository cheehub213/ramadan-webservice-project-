"""
Chat Service - Handles imam chat and conversation management
"""
from sqlalchemy.orm import Session
from datetime import datetime

class ChatService:
    
    # Default imams in system
    DEFAULT_IMAMS = [
        {
            "name": "Imam Ahmad",
            "email": "imam.ahmad@mosque.local",
            "expertise": "Quran & Islamic Law",
            "is_available": True,
            "bio": "Expert in Quranic interpretation and Islamic jurisprudence"
        },
        {
            "name": "Imam Mohammed",
            "email": "imam.mohammed@mosque.local",
            "expertise": "Hadith & Islamic History",
            "is_available": True,
            "bio": "Specialist in authentic hadith and Islamic history"
        },
        {
            "name": "Imam Fatima",
            "email": "imam.fatima@mosque.local",
            "expertise": "Women's Islamic Issues",
            "is_available": True,
            "bio": "Expert in women's issues in Islam and family matters"
        }
    ]
    
    @staticmethod
    def get_all_imams(db: Session):
        """Get list of all imams"""
        from models_extended import Imam
        
        imams = db.query(Imam).all()
        if not imams:
            # Initialize with default imams if none exist
            for imam_data in ChatService.DEFAULT_IMAMS:
                imam = Imam(**imam_data)
                db.add(imam)
            db.commit()
            imams = db.query(Imam).all()
        return imams
    
    @staticmethod
    def get_imam_by_id(db: Session, imam_id: int):
        """Get specific imam details"""
        from models_extended import Imam
        
        return db.query(Imam).filter(Imam.id == imam_id).first()
    
    @staticmethod
    def create_conversation(db: Session, user_email: str, imam_id: int, topic: str):
        """Create new conversation between user and imam"""
        from models_extended import Conversation, User, Imam
        
        # Ensure user exists
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            user = User(email=user_email, user_type="user")
            db.add(user)
            db.commit()
        
        # Verify imam exists
        imam = db.query(Imam).filter(Imam.id == imam_id).first()
        if not imam:
            raise ValueError(f"Imam with ID {imam_id} not found")
        
        # Create conversation
        conversation = Conversation(
            user_id=user.id,
            user_email=user_email,
            imam_id=imam_id,
            topic=topic
        )
        db.add(conversation)
        db.commit()
        return conversation
    
    @staticmethod
    def send_message(db: Session, conversation_id: int, sender_email: str, sender_type: str, message_text: str):
        """Send a message in conversation"""
        from models_extended import Message, Conversation
        
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        message = Message(
            conversation_id=conversation_id,
            sender_email=sender_email,
            sender_type=sender_type,
            message_text=message_text,
            imam_id=conversation.imam_id if sender_type == "imam" else None
        )
        db.add(message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.now()
        
        # If user sent message, mark imam's previous messages as read
        if sender_type == "user":
            prev_messages = db.query(Message).filter(
                Message.conversation_id == conversation_id,
                Message.sender_type == "imam"
            ).all()
            for msg in prev_messages:
                msg.is_read = True
        
        db.commit()
        return message
    
    @staticmethod
    def get_conversation_messages(db: Session, conversation_id: int):
        """Get all messages in a conversation"""
        from models_extended import Message
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        return messages
    
    @staticmethod
    def get_user_conversations(db: Session, user_email: str):
        """Get all conversations for a user"""
        from models_extended import Conversation
        
        conversations = db.query(Conversation).filter(
            Conversation.user_email == user_email
        ).order_by(Conversation.updated_at.desc()).all()
        return conversations
    
    @staticmethod
    def get_unread_message_count(db: Session, conversation_id: int, viewer_type: str):
        """Get count of unread messages"""
        from models_extended import Message
        
        if viewer_type == "user":
            unread = db.query(Message).filter(
                Message.conversation_id == conversation_id,
                Message.sender_type == "imam",
                Message.is_read == False
            ).count()
        else:
            unread = db.query(Message).filter(
                Message.conversation_id == conversation_id,
                Message.sender_type == "user",
                Message.is_read == False
            ).count()
        
        return unread
    
    @staticmethod
    def generate_imam_response(message: str, imam_name: str) -> str:
        """Generate an imam response using simple logic (can be enhanced with AI)"""
        responses = [
            f"Wa alaikum assalam wa rahmatullahi wa barakatuh. Thank you for reaching out. That's a thoughtful question.",
            f"May Allah bless you. I appreciate your concern. Let me share some Islamic perspective on this.",
            f"Wa alaikum assalam. This is an important matter. Here's what our Islamic scholars say...",
            f"Thank you for this question. In Islam, we are guided by the Quran and Sunnah...",
            f"May Allah guide us all. Based on Islamic teachings and the wisdom of the Prophet...",
        ]
        import random
        return random.choice(responses)
