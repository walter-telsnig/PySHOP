from Plots import *

def save_results(shop, file_path_root, file_path_detail,topology,Short_Term=False):

    starttime = shop.get_time_resolution()['starttime']
    endtime = shop.get_time_resolution()['endtime']

    print("Save overview")
    plot_storage_results(shop,starttime,endtime)
    plt.savefig(file_path_root +"storage_overview.pdf")
    plt.close()

    if Short_Term:
        plot_production_results(shop, starttime, endtime, daily_avg_price=False)
    else:
        plot_production_results(shop,starttime,endtime,daily_avg_price=True)
    plt.savefig(file_path_root +"production_overview.pdf")
    plt.close()

    num_months = int(np.ceil((endtime-starttime)/np.timedelta64(1, 'M')))
    for m in np.arange(0,num_months):
        st = pd.Timestamp(starttime.year,starttime.month,1)+pd.DateOffset(months=m)
        print("Save monthly overview: " + str(st.month) + "-" + str(st.year))
        plot_storage_results(shop,  starttime=st, endtime=st+pd.DateOffset(months=1))
        plt.savefig(file_path_detail + "storage_" + str(st.year) + "_" + str(st.month) + ".pdf")
        plt.close()

        plot_production_results(shop, starttime=st, endtime=st+pd.DateOffset(months=1), daily_avg_price=False)
        plt.savefig(file_path_detail + "production_" + str(st.year) + "_" + str(st.month) + ".pdf")
        plt.close()

    print("Save time series")
    create_dataframe_for_export(shop,file_path_root,topology)