class CollectionPolicy:
    
    def can_update(self, profile, collection):
        if profile is None:
            return False
        
        return collection.creator_id == profile.id
    
    def can_delete(self, profile, collection):
        if profile is None:
            return False
        
        return collection.creator_id == profile.id