"""
Enhanced Early Warning System (EWS)
Identifies students at risk of dropping out or failing
"""

class EnhancedEWSService:
    """Service for identifying at-risk students"""
    
    def __init__(self):
        self.risk_indicators = {}
        self.alerts = []
    
    def analyze_student_risk(self, student_id, attendance_rate, grade_average, behavior_score):
        """
        Analyze risk factors for a student
        
        Args:
            student_id (str): Student ID
            attendance_rate (float): Attendance percentage (0-100)
            grade_average (float): Average grade (0-100)
            behavior_score (float): Behavior score (0-100)
            
        Returns:
            dict: Risk assessment
        """
        try:
            risk_level = "Low"
            risk_score = 0
            factors = []
            
            # Attendance analysis
            if attendance_rate < 80:
                risk_score += 30
                factors.append("Low attendance")
            
            # Grade analysis
            if grade_average < 60:
                risk_score += 35
                factors.append("Low grades")
            elif grade_average < 75:
                risk_score += 15
            
            # Behavior analysis
            if behavior_score < 60:
                risk_score += 25
                factors.append("Poor behavior")
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = "High"
            elif risk_score >= 40:
                risk_level = "Medium"
            
            assessment = {
                'student_id': student_id,
                'risk_level': risk_level,
                'risk_score': risk_score,
                'factors': factors,
                'recommendations': self._get_recommendations(risk_level)
            }
            
            self.risk_indicators[student_id] = assessment
            
            if risk_level in ["High", "Medium"]:
                self.alerts.append({
                    'student_id': student_id,
                    'risk_level': risk_level,
                    'message': f"Student {student_id} identified as {risk_level} risk"
                })
            
            return assessment
        except Exception as e:
            print(f"Error analyzing student risk: {e}")
            return None
    
    def _get_recommendations(self, risk_level):
        """Get recommendations based on risk level"""
        recommendations = {
            'Low': ['Continue monitoring', 'Maintain current support'],
            'Medium': ['Increase monitoring', 'Provide tutoring', 'Parent communication'],
            'High': ['Urgent intervention', 'Counseling referral', 'Intensive support', 'Parent meeting']
        }
        return recommendations.get(risk_level, [])
    
    def get_at_risk_students(self):
        """Get list of at-risk students"""
        try:
            at_risk = [s for s in self.risk_indicators.values() if s['risk_level'] in ['High', 'Medium']]
            return sorted(at_risk, key=lambda x: x['risk_score'], reverse=True)
        except Exception as e:
            print(f"Error getting at-risk students: {e}")
            return []
    
    def get_alerts(self):
        """Get all alerts"""
        return self.alerts
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts = []

# Create a singleton instance
_ews_service = None

def get_ews_service():
    """Get or create the EWS service instance"""
    global _ews_service
    if _ews_service is None:
        _ews_service = EnhancedEWSService()
    return _ews_service
