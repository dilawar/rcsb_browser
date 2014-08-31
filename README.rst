A command line browser for RCSB data bank: you can either query the their
database for keywords or download PDB file when ID is known. This version only
downloads the pdb file in tar.gz file.

USAGE EXAMPLE
=============

To query

::
    $ rcsb_browser --query adenine in human by Hurley and Parajuli

    Total 1 results are fetched
    INFO: Storing custom report: /home/dilawar/Work/GITHUB/rcsb_browser

    ++++++++++
                  structureId : 4L2O
               structureTitle : Crystal structure of human ALDH3A1 with its selective inhibitor 1-(4-fluorophenyl)sulfonyl-2-methylbenzimidazole
        experimentalTechnique : X-RAY DIFFRACTION
               depositionDate : 2013-06-04
                  releaseDate : 2014-01-29
                        ndbId : null
                   resolution : 1.94
              structureAuthor : Hurley, T.D., Parajuli, B.
               classification : OXIDOREDUCTASE/Inhibitor
     structureMolecularWeight : 213310.03
            macromoleculeType : Protein


In this example, only one result is fetched but if query is short then you might
end up getting thousands for results (though it will never print more than 100
results onto the console). A file in XML format is also saved which you can open
in some office-suite to see.

Once ID is known (e.g. 4l20 in this case), you can download the pdb file, by
using the --fetch (or -f) command.

::
    $ rcsb_browser --fetch 4l20

It will download and store the file in current working directory.
