import uuid
import json
import random
from sqlalchemy.orm import Session
from .. import models

class MockNDUService:
    def __init__(self, db: Session):
        self.db = db

    def sync_content(self, content: models.ContentItem):
        # Simulate payload
        payload = {
            "title": content.title,
            "category": content.category,
            "duration": content.duration_minutes,
            "source": "SAMARTH_PORTAL"
        }
        
        # Mock API Call logic with Retry (Clause 4.6)
        max_retries = 3
        for attempt in range(max_retries):
            # random failure simulation removed for deterministic demo, but structure supports it
            is_success = True 
            
            if is_success:
                mock_id = f"NDU-{uuid.uuid4().hex[:8].upper()}"
                response = {"id": mock_id, "status": "Synced", "message": "Content received successfully"}
                
                # Update local entity
                content.ndu_reference_id = mock_id
                self.db.add(content)
                self.db.commit()
                
                self._log_integration("SYNC_CONTENT", payload, response, "SUCCESS")
                return True, "Successfully synced with NDU"
            
            # If failed, we would continue
        
        # If loop finishes without success
        response = {"error": "Gateway Timeout", "code": 504}
        self._log_integration("SYNC_CONTENT", payload, response, "FAILURE", "Max retries exceeded")
        return False, "Failed to sync with NDU"

    # Progress Sync Logic (Clause 4.6 Hardening)
    def sync_progress(self, batch_id: int, progress_data: dict, user_id: int):
        payload = {
            "type": "BATCH_PROGRESS",
            "batch_id": batch_id,
            "data": progress_data,
            "timestamp": "2024-03-20T10:00:00Z"
        }
        # Simulate Network Call
        import random
        success = random.choice([True, True, False]) # 66% success chance
        
        response = {"status": "ACK", "message": "Progress Updated"} if success else {"error": "Sync Failed"}
        status_code = "SUCCESS" if success else "FAILURE"
        
        self._log_integration("SYNC_PROGRESS", payload, response, status_code)
        
        # Log to Audit Trail as well (RFP Requirement)
        from .. import crud
        crud.log_audit(self.db, user_id, "SYNC_PROGRESS", f"Synced progress for Batch {batch_id}: {status_code}")
        
        return success, response

    def sync_training(self, training: models.TrainingProgram):
        payload = {
            "program_name": training.title,
            "instructor": training.instructor,
            "date": training.date,
            "participants": training.participants_count
        }
        
        # Mock API Call
        is_success = True
        
        if is_success:
            mock_id = f"NDU-TR-{uuid.uuid4().hex[:8].upper()}"
            response = {"id": mock_id, "status": "Scheduled", "message": "Training program registered"}
            
            # Update local entity
            training.ndu_mapping_id = mock_id
            self.db.add(training)
            self.db.commit()
            
            self._log_integration("SYNC_TRAINING", payload, response, "SUCCESS")
            return True, "Successfully synced with NDU"
        
        return False, "Failed to sync"

    def _log_integration(self, endpoint, payload, response, status, error=None):
        log_entry = models.IntegrationLog(
            endpoint=endpoint,
            payload=json.dumps(payload),
            response=json.dumps(response),
            status=status,
            error=error
        )
        self.db.add(log_entry)
        self.db.commit()
