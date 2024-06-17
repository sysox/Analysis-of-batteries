######################################################### Names ########################################################

batteries = ["Dieharder", "NIST", "TestU01"]
subbatteries = ["Diehard", "Dieharder", "NIST_STS", "Small_Crush", "Crush", "Rabbit", "Alphabit", "Block_Alphabit"]
subbatteries_abreviations = ["Drd", "Drd", "STS", "SC", "C", "R", "A", "BA" ]
GoFs = ["dieharder_default", "dieharder_kuiper", "nist_chi2", "testu01_snpair_ClosePairs",
        "testu01_sknuth_MaxOft", "testu01_ksp", "testu01_ksm", "testu01_ks",
        "testu01_ad", "testu01_cm", "testu01_wg", "testu01_wu", "marsa_KS_left",
        "marsa_KS_right", "marsa_KS_both", "dieharder_corrected", "dieharder_fast"]

files_names_examples = ["Dieharder(4) Diehard Bitstream Test.pval",
                        "Dieharder(208) DAB Fill Tree Test 2 Subtest 2.pval",
                        "Dieharder(200-8) RGB Bit Distribution Test.pval",
                        "NIST Statistical Testing Suite(3) Cumulative Sum (Cusum) Test Subtest 1.pval",
                        "NIST Statistical Testing Suite(7) Discrete Fourier Transform (Spectral) Test.pval",
                        "TestU01 Alphabit(2) smultin_MultinomialBitsOver.pval",
                        "TestU01 Alphabit(9) swalk_RandomWalk1-P1.pval",
                        "TestU01 Block Alphabit(1-2) smultin_MultinomialBitsOver.pval",
                        "TestU01 Block Alphabit(8-1) swalk_RandomWalk1-P1.pval",
                        "TestU01 Crush(20) snpair_ClosePairs-P4.pval",
                        "TestU01 Crush(1) smarsa_SerialOver.pval",
                        "TestU01 Rabbit(12) sstring_HammingCorr.pval",
                        "TestU01 Rabbit(25) swalk_RandomWalk1-P5.pval",
                        "TestU01 Small Crush(4) sknuth_SimpPoker.pval",
                        "TestU01 Small Crush(10) swalk_RandomWalk1-P1.pval"]

######################################################### Functions ####################################################
def extract_from_path(path):
    '''
    extracts all relevant data from file name "TestU01 Small Crush(10) swalk_RandomWalk1-P1.pval"
    - battery name, subbattery name, test name, test id as string "id1|id2|id3"
    '''
    filename = path.split('/')[-1].split('.pval')[0]
    idx1, idx2 = filename.find('('), filename.find(')')
    test_id = filename[idx1+1:idx2]
    name_subtest = filename[idx2+1:]

    # id parsing
    if '-' in test_id:
        id = test_id.split('-')
    else:
        id = [test_id, "0" ]
    result_id = 0
    if '-' in name_subtest:
        test, pvalue_number = name_subtest.split('-')
        result_id = pvalue_number.split('P')[1]
    else:
        test = name_subtest
    id = id + [result_id]
    id = list(map(int, id))
    id_string = "{:03d}".format(id[0]) + "|" + "{:03d}".format(id[1]) + "|" + "{:03d}".format(int(id[2]))

    # battery
    battery = filename.split('(')[0].split(' ')[0]

    # subbattery name
    if battery == 'Dieharder':
        subbattery = 'Dieharder' if id[0] < 100 else 'Diehard'
    else:
        subbattery = '_'.join(filename.split('(')[0].split(' ')[1:])
    return battery, subbattery, test, id_string


# uniform_pvals_WSL_path = 'mnt/d/Data/pvals/pvals/uniform_virtual_test/pvals'
# uniform_pvals_Windows_path = 'D:\Data\pvals\pvals\uniform_virtual_test\pvals'
dll_path = '/mnt/c/Users/user/PycharmProjects/Analysis-of-batteries/src/C/libpvals.so'
GoF_test_ids = list(range(17))

GoF_test_names = {0:"dieharder_pvalue", 1:"dieharder_pvalue_kuiper", 2:"nist_pvalue", 3:"testu01_pvalue_snpair_ClosePairs",
       4:"testu01_pvalue_sknuth_MaxOft", 5:"testu01_pvalue_ksp", 6:"testu01_pvalue_ksm", 7:"testu01_pvalue_ks",
       8:"testu01_pvalue_ad", 9:"testu01_pvalue_cm", 10:"testu01_pvalue_wg", 11:"testu01_pvalue_wu",
        12:"marsa_KS_left_pvalue", 13:"marsa_KS_right_pvalue", 14:"marsa_both_pvalue", 15:"dieharder_corrected_pvalue",
        16:"dieharder_fast_pvalue"}

# def testname_to_GoF_idx(test_name):
#     if 'Diehard' in test_name:
#         return 0
#     if  'NIST' in test_name:
#         return 2
#     if 'snpair_ClosePairs-1stP' in test_name:
#         return 3
#     if 'sknuth_MaxOft-1stP' in test_name:
#         return 4
#     if 'TestU01' in test_name:
#         return -1
#     return -1


if __name__ == "__main__":
    #     testing names of files
    for file in files_names_examples:
        battery, subbattery, test, id = extract_from_path(file)
        print(battery, subbattery, test, id)




