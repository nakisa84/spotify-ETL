from avg_album_length_playlist import gather_data_local,gather_data



if __name__ == '__main__' : 
    PLAYLIST1 = 'rap_caviar'
    PLAYLIST2 = 'relax_and_chill'
    PLAYLIST3 = 'best_of_2000_pop'
    PLAYLIST4 = 'iranian_rap'
    playlists =  [PLAYLIST1,PLAYLIST2,PLAYLIST3,PLAYLIST4]
    for item in playlists:
        gather_data(item)

