from avg_album_length_playlist import gather_data,create_recommended_playlist,read_data
import requests
import config.variables


if __name__ == '__main__' : 
    # PLAYLIST1 = 'rap_caviar'
    # PLAYLIST2 = 'relax_and_chill'
    # PLAYLIST3 = 'best_of_2000_pop'
    # PLAYLIST4 = 'iranian_rap'
    # playlists =  [PLAYLIST1,PLAYLIST2,PLAYLIST3,PLAYLIST4]
    # for item in playlists:
    #     gather_data(item)
    # create_recommended_playlist()



    # auth_response = requests.post(config.variables.AUTH_URL,{
    # 'grant_type':'client_credentials',
    # 'client_id': config.variables.CLIENT_ID,
    # 'client_secret': config.variables.CLIENT_SECRET
    #  })

    # auth_response_data = auth_response.json()
    # access_token = auth_response_data['access_token']
    # headers = {
    #         'Authorization': f'Bearer {access_token}'
    #     }
    # url = 'https://api.spotify.com/v1/browse/featured-playlists?locale=fa_IR'    
    
    # r = requests.get(url, headers=headers)
    # d = r.json()
    # print('done')

  read_data('2022/8/7','iranian_rap.csv','spotify-analysis-data-nakisa')