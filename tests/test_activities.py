"""
Tests for the High School Activities API using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_all_activities_returns_ok(self, client):
        """Test that GET /activities returns status 200."""
        # Arrange: no setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        # Arrange: no setup needed
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert isinstance(data, dict)
        assert len(data) > 0
    
    def test_get_activities_contains_expected_activities(self, client):
        """Test that all expected activities are returned."""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Science Club"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity in expected_activities:
            assert activity in data
    
    def test_get_activities_has_required_fields(self, client):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Missing {field} in {activity_name}"
            assert isinstance(activity_data["participants"], list)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_participant_returns_ok(self, client):
        """Test signing up a new participant returns 200."""
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_signup_new_participant_returns_message(self, client):
        """Test that signup returns a success message."""
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds the participant to the activity."""
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email in activities[activity]["participants"]
    
    def test_signup_duplicate_participant_returns_400(self, client):
        """Test that signing up an already registered participant returns 400."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_signup_duplicate_participant_error_message(self, client):
        """Test that duplicate signup has appropriate error message."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "already signed up" in data["detail"]
    
    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signing up for non-existent activity returns 404."""
        # Arrange
        activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_signup_invalid_activity_error_message(self, client):
        """Test that invalid activity has appropriate error message."""
        # Arrange
        activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "not found" in data["detail"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""
    
    def test_unregister_existing_participant_returns_ok(self, client):
        """Test that unregistering an existing participant returns 200."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_unregister_existing_participant_returns_message(self, client):
        """Test that unregister returns a success message."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert "Unregistered" in data["message"]
    
    def test_unregister_removes_participant_from_activity(self, client):
        """Test that unregister actually removes the participant."""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email not in activities[activity]["participants"]
    
    def test_unregister_nonexistent_participant_returns_400(self, client):
        """Test that unregistering a non-registered participant returns 400."""
        # Arrange
        activity = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
    
    def test_unregister_nonexistent_participant_error_message(self, client):
        """Test that unregistering non-registered participant has error message."""
        # Arrange
        activity = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "not signed up" in data["detail"]
    
    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404."""
        # Arrange
        activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404


class TestSignupUnregisterIntegration:
    """Integration tests for signup and unregister workflows."""
    
    def test_signup_then_unregister_flow(self, client):
        """Test the complete flow: signup, verify, unregister, verify."""
        # Arrange
        activity = "Drama Club"
        email = "testuser@mergington.edu"
        
        # Act & Assert: Register
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Act & Assert: Verify registered
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]
        
        # Act & Assert: Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Act & Assert: Verify unregistered
        activities = client.get("/activities").json()
        assert email not in activities[activity]["participants"]
    
    def test_signup_unregister_then_signup_again(self, client):
        """Test that participant can sign up again after unregistering."""
        # Arrange
        activity = "Tennis Club"
        email = "testuser@mergington.edu"
        
        # Act: First signup
        client.post(f"/activities/{activity}/signup", params={"email": email})
        
        # Act: Unregister
        client.delete(f"/activities/{activity}/signup", params={"email": email})
        
        # Act: Second signup
        second_signup = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert: Second signup succeeds
        assert second_signup.status_code == 200
        
        # Assert: Participant is registered again
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]
