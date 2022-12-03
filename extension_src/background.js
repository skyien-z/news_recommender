const server_host = "http://127.0.0.1:8000";      // localhost; Django's server root
const path_to_query = "/twitter_connect/get_news_articles/?tweet_id=";
const no_hyperlink_in_text_error = "There are no news articles in this tweet";
const wrong_site_msg = "Unfortunately, you are not on a twitter status session. You are here: "
const notification_icon = "news-icon.png";
const tweet_id_error = -1

function get_tweet_id(url_str) {
    const url = new URL(url_str);
    var url_array = url_str.split('/')

    const is_host_twitter = url.hostname.toLowerCase().includes("twitter.com");
    const is_tweet_selected = url_array[url_array.length - 2] == "status";

    if (is_host_twitter && is_tweet_selected) {
        return url_array[url_array.length - 1]
    }

    console.error(wrong_site_msg + url_str);
    return tweet_id_error
}

function recommend_news(url_str) {
    const tweet_id = get_tweet_id(url_str)
    if (tweet_id == tweet_id_error) { return }

    console.error(tweet_id)
    const server_query_url = server_host + path_to_query + encodeURIComponent(tweet_id);
    fetch(server_query_url)
    .then(response => response.json())
    .then((data) => {               // JSON of singular returned article
        if (data.title == no_hyperlink_in_text_error) {
            console.error(no_hyperlink_in_text_error)
            return
        }

        var notifOptions = {
            iconUrl: notification_icon,
            type: 'basic',
            title: data.title,
            message: data.description
        };
        
        chrome.notifications.create(data.url, notifOptions);
        chrome.notifications.onClicked.addListener(function(notificationId) {
            chrome.tabs.create({url: notificationId});
            });  

    }).catch(error => console.log(error));
}

chrome.tabs.onActivated.addListener( function(activeInfo){
    chrome.tabs.get(activeInfo.tabId, function(tab) {
        recommend_news(tab.url)
    });
});

chrome.tabs.onUpdated.addListener((tabId, change, tab) => {
    if (tab.active && change.url) {
        recommend_news(tab.url)  
    }
});

