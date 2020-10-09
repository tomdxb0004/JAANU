# qty
def cap_split_allocate(capital,ltp,no_of_best_candidates):
    cap_split = capital/no_of_best_candidates
    cap_split = 0.9 * cap_split
    return round(cap_split/ltp,0)

# from best candidates pick stock to enter
def pick_stock(no_of_best_candidates,dataframe):
      
    if no_of_best_candidates>0:
        print(dataframe)
        todays_pick = dataframe
        
        return todays_pick
