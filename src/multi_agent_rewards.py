class MultiAgentRewardTracker:
    def __init__(self):
        self.agent_scores = {
            'planning_effectiveness': 0.0,
            'execution_accuracy': 0.0,
            'verification_precision': 0.0
        }
        
    def update_scores(self, step_data):
        # Simple heuristics based on step success
        if step_data.get('reasoning_quality', 0) > 0.7:
            self.agent_scores['planning_effectiveness'] += 0.1
        if step_data.get('action_success', False):
            self.agent_scores['execution_accuracy'] += 0.15
        if step_data.get('state_validated', False):
            self.agent_scores['verification_precision'] += 0.1
            
    def get_breakdown(self):
        return {
            "total_reward": sum(self.agent_scores.values()),
            "breakdown": self.agent_scores,
            "insights": self._generate_insights()
        }
        
    def _generate_insights(self):
        max_score = max(self.agent_scores.values())
        min_score = min(self.agent_scores.values())
        
        if max_score > min_score * 2:
            weak_agent = min(self.agent_scores, key=self.agent_scores.get)
            return f"Bottleneck detected in {weak_agent.replace('_', ' ')}"
        return "Balanced performance across agents"

# Demo usage
if __name__ == "__main__":
    tracker = MultiAgentRewardTracker()
    
    # Simulate some steps
    tracker.update_scores({'reasoning_quality': 0.8, 'action_success': True, 'state_validated': True})
    tracker.update_scores({'reasoning_quality': 0.6, 'action_success': False, 'state_validated': True})
    
    print("🤖 Multi-Agent Reward Breakdown:")
    result = tracker.get_breakdown()
    print(f"   Total: {result['total_reward']:.2f}")
    print("   Breakdown:")
    for agent, score in result['breakdown'].items():
        print(f"     {agent.replace('_', ' ').title()}: +{score:.2f}")
    print(f"   💡 Insight: {result['insights']}")
