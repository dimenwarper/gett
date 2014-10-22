crit <-
function(theta, S,n, lambda1, lam2, penalize.diagonal)  # theta = list of pXp matrices, length k
{
	p = dim(S[[1]])[1]
	K = length(S)
	if(is.list(lambda1)){
		lam1 = list()
		for(i in 1:length(lambda1)){lam1[[i]] = penalty.as.matrix(lambda1[[i]],p,penalize.diagonal=penalize.diagonal)}
	}
	else{lam1 = penalty.as.matrix(lambda1,p,penalize.diagonal=penalize.diagonal)}
	lam2 = penalty.as.matrix(lam2,p,penalize.diagonal=TRUE)	
	crit = 0
	for(k in 1:length(theta))
	{
		# add log det that was entered as an argument, or else calculate it
		if(is.list(lam1)){
			crit = crit+n[k]*log(det(theta[[k]]))-n[k]*sum(S[[k]]*theta[[k]])-sum(lam1[[k]]*abs(theta[[k]])) 
		}
		else{
			crit = crit+n[k]*log(det(theta[[k]]))-n[k]*sum(S[[k]]*theta[[k]])-sum(lam1*abs(theta[[k]])) 
		}
		for(kp in k:length(theta))
		{
			crit = crit - sum(lam2*abs(theta[[k]]-theta[[kp]]))
		}
	}
	return(crit)
}

