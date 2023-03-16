import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import React from 'react';

function Toolbar() {
    
    return (
        <div> 
            <List open={true}>
                <ListItemButton> Click me </ListItemButton>
                <ListItemButton> Touch me </ListItemButton>
                <ListItemButton> Lick me </ListItemButton>
            </List>
        </div>

    )
}

export default Toolbar
