#!/bin/bash
echo "⚠️  WARNING: This will delete repositories!"
echo "Repositories to delete:"
echo "  - ~/humbu_community_nexus/"

read -p "Are you sure? (yes/no): " confirm
if [ "$confirm" = "yes" ]; then
    echo "Creating final backup before deletion..."
    cp instance/imperial.db "imperial_final_$(date +%Y%m%d_%H%M%S).db"
    
    echo "Deleting repositories..."
    rm -rf ~/humbu_community_nexus/
    
    echo "✅ Cleanup complete!"
    df -h ~/
else
    echo "Cleanup cancelled"
fi
