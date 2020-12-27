CS = 1
def _async_iter_seats(data, indexs):
    with Pool(processes=6) as pool:
        indexs = np.array(indexs).T
        print('here1')
        empties_future = pool.starmap(empty, indexs, chunksize=CS)
        print('here2')
        fulls_future = pool.starmap(full, indexs, chunksize=CS)
        print('here3')
#         empties_future.wait()
#         print('here4')
#         fulls_future.wait()
#         print('here5')
    empties = empties_future.get()
    fulls = fulls_future.get()
    return empties, fulls
        